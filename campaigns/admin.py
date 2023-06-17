from django.contrib import admin

from .models import Campaign, Choice

admin.site.site_header = "e-voting Admin"
admin.site.site_title = "e-voting Admin Area"
admin.site.index_title = "Welcome to the e-voting admin area"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class CampaignAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['campaign_text']}),
                 ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}), ]
    inlines = [ChoiceInline]


# admin.site.register(Campaign)
# admin.site.register(Choice)
admin.site.register(Campaign, CampaignAdmin)