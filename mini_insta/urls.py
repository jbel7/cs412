# URL pattern for mini_insta app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='show_post'),
]