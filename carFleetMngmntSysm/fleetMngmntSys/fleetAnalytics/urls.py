from django.urls import path
from .views import analytics

app_name = "fleetAnalytics"


urlpatterns = [
    path("fleetAnalytics/analytics/", analytics, name="analytics"),
]
