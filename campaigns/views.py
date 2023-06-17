from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Campaign, CampaignVote
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import transaction
from users.models import User

from django.db.models import Count

# Get campaigns and display them
@login_required
def home(request):
    campaign_queryset = Campaign.objects.filter(voters=request.user).order_by('-created_on')
    context = {'campaign_queryset': campaign_queryset,'len':len(campaign_queryset)}
    return render(request, 'campaigns/index.html', context)

# Show specific campaign and choices
@login_required
def detail(request, campaign_id):
  try:
    campaign = Campaign.objects.get(pk=campaign_id)
  except Campaign.DoesNotExist:
    raise Http404("Campaign does not exist")
  return render(request, 'campaigns/detail.html', { 'campaign': campaign })

# Get campaign and display results
@login_required
def results(request, campaign_id):
  result={}
  campaign = get_object_or_404(Campaign, pk=campaign_id)
  for i in CampaignVote.objects.filter(campaign=campaign):
     if i.candiate.username in result:
        result[i.candiate.username]+=1
     else:
        result[i.candiate.username]=1
  print(result)

  return render(request, 'campaigns/results.html', { 'campaign': campaign ,'result':result})

# Vote for a campaign choice
@login_required
def vote(request, campaign_id):
    # print(request.POST['choice'])
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    if CampaignVote.objects.filter(voter=request.user,campaign=campaign).exists():
       return render(request, 'campaigns/detail.html', {
            'campaign': campaign,
            'error_message': "Already gave the vote.",
        })
    try:
        selected_choice = campaign.candidates.get(pk=request.POST['choice'])
    except (KeyError, User.DoesNotExist):
        # Redisplay the campaign voting form.
        return render(request, 'campaigns/detail.html', {
            'campaign': campaign,
            'error_message': "You didn't select a choice.",
        })
    if selected_choice == request.user:
       return render(request, 'campaigns/detail.html', {
            'campaign': campaign,
            'error_message': "Cant Vote for Yourself",
        })
    else:
        try:
          with transaction.atomic():
            CampaignVote.objects.create(voter=request.user,campaign=campaign,candiate=selected_choice)
        except Exception as err:
           return render(request, 'campaigns/detail.html', {
            'campaign': campaign,
            'error_message': "Problem in DataBase",
        })

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('campaigns:campaign_results', args=(campaign.id,)))

@login_required
def resultsData(request, obj):
    print("Coming Here")
    votedata = []
    campaign = Campaign.objects.get(id=obj)
    print(campaign)
    try:
      votes=CampaignVote.objects.filter(campaign=campaign).values('candiate','id').aggregate(Count(id))
    except Exception as err:
       print(err)
    print(votes)

    for i in votes:
        votedata.append({i.choice_text:i.votes})

    # return JsonResponse(votedata, safe=False)
