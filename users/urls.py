from django.urls import path
from .views import role_based_redirect

urlpatterns = [
    path('redirect/', role_based_redirect, name='role_based_redirect'),
    # Other user-related URLs
]
