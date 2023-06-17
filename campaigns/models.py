from django.db import models


class Campaign(models.Model):
    campaign_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.campaign_text


class Choice(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
