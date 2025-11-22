from django.urls import path
from .views import get_reports

app_name = "dailyreports_api"

urlpatterns = [
    path("reports/", get_reports, name="reports"),
]
