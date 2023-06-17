from django.urls import path

from .views import home,detail,results,vote,resultsData

app_name = 'campaigns'
urlpatterns = [
    path('',   home, name='home'),
    path('<int:campaign_id>/',   detail, name='campaign_detail'),
    path('<int:campaign_id>/results/',   results, name='campaign_results'),
    path('<int:campaign_id>/vote/',   vote, name='campaign_vote'),
    path('resultsdata/<str:obj>/',   resultsData, name='campaign_resultsdata'),
]
