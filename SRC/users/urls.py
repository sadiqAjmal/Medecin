from django.urls import path
from .views import role_based_redirect

urlpatterns = [
    path('', role_based_redirect, name='redirect'),
]
