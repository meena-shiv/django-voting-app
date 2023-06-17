from django.contrib import admin

from .models import Campaign, Choice

admin.site.site_header = "Campagin Admin"
admin.site.site_title = "Campagin Admin Area"
admin.site.index_title = "Welcome to the e-voting Campaign Are"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class CampaignAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['campaign_text']}),
                #  ('Date Information', {'fields': ['created_on'], 'classes': ['collapse']}), 
                 ]
    inlines = [ChoiceInline]


# admin.site.register(Campaign)
# admin.site.register(Choice)
admin.site.register(Campaign, CampaignAdmin)