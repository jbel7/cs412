from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.

# Adds the overall view of all profiles
class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

# Adds the detail view to profiles
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'