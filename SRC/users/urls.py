from django.urls import path
from .views import role_based_redirect

'''
url patterns for the users app, these urls are used to navigate through the application,
- redirect: redirect view
Based on the role of the user, the user is redirected to the respective dashboard
'''
urlpatterns = [
    path('', role_based_redirect, name='redirect'),
]
