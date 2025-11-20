from django.urls import path
from . import views

urlpatterns = [
    # 📚 Added URL patterns for the Tables Dropdown Menu
    path('daily_reports/psp/', views.psp, name='psp'),
    path('daily_reports/error_report/', views.error_report, name='error_report'),
    path('daily_reports/monthly_error_report/', views.monthly_error_report, name='monthly_error_report'),
]