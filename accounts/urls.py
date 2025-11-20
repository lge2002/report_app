# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),

    # use the function-based login view (keeps your current logic)
    path('login/', views.login_view, name='login'),

    # if you prefer the class-based StateAwareLoginView, replace the above line with:
    # path('login/', views.StateAwareLoginView.as_view(), name='login'),

    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('select_state/', views.select_state, name='select_state'),
]
