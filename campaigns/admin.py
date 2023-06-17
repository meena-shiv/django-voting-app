from django.contrib import admin

from .models import Campaign

admin.site.site_header = "Campagin Admin"
admin.site.site_title = "Campagin Admin Area"
admin.site.index_title = "Welcome to the e-voting Campaign Are"


class CampaignAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['campaign_text']}),
                 ('Candiatates', {'fields': ['candidates']}),
                 ('Voters', {'fields': ['voters']}), 
                 ]


# admin.site.register(Campaign)
# admin.site.register(Choice)
admin.site.register(Campaign, CampaignAdmin)