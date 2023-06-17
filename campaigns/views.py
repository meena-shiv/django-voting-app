from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Campaign, Choice
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.http import Http404

# Get campaigns and display them
@login_required
def home(request):
    campaign_queryset = Campaign.objects.order_by('-pub_date')[:5]
    context = {'campaign_queryset': campaign_queryset}
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
  campaign = get_object_or_404(Campaign, pk=campaign_id)
  return render(request, 'campaigns/results.html', { 'campaign': campaign })

# Vote for a campaign choice
@login_required
def vote(request, campaign_id):
    # print(request.POST['choice'])
    campaign = get_object_or_404(Campaign, pk=campaign_id)
    try:
        selected_choice = campaign.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the campaign voting form.
        return render(request, 'campaigns/detail.html', {
            'campaign': campaign,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('campaigns:results', args=(campaign.id,)))

@login_required
def resultsData(request, obj):
    votedata = []

    campaign = Campaign.objects.get(id=obj)
    votes = campaign.choice_set.all()

    for i in votes:
        votedata.append({i.choice_text:i.votes})

    return JsonResponse(votedata, safe=False)
