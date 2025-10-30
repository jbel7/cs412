# File: voter_analytics/urls.py
# Name: Jed Belsany
# BU email: belsanyj@bu.edu
# Description: URL configuration for voter analytics application

from django.urls import path
from .views import VoterListView, VoterDetailView

app_name = 'voter_analytics'
urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
]