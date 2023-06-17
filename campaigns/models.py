from django.db import models
from django.contrib.auth.models import User


class Campaign(models.Model):
    campaign_text = models.CharField(max_length=500)
    created_on = models.DateTimeField(auto_now_add=True)
    candidates = models.ManyToManyField(User,related_name='campaign_candidates')
    voters = models.ManyToManyField(User,related_name='campaign_voters')

    def __str__(self):
        return self.campaign_text

class CampaignVote(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    candiate = models.ForeignKey(User, on_delete=models.CASCADE,related_name='campaignvote_candiate')
    voter = models.ForeignKey(User, on_delete=models.CASCADE,related_name='campaignvote_voter')
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='campaign_vote'
