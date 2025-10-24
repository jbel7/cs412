# URL pattern for mini_insta app
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public URLs (no login required)
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/followers', views.ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following', views.ShowFollowingDetailView.as_view(), name='show_following'),
    path('create_profile', views.CreateProfileView.as_view(), name='create_profile'),

    # Protected URLs (login required)
    path('profile/create_post', views.CreatePostView.as_view(), name='create_post'),
    path('profile/update', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/feed', views.PostFeedListView.as_view(), name='show_feed'),
    path('profile/search', views.SearchView.as_view(), name='search'),

    # Post operations (login required)
    path('post/<int:pk>/delete', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update', views.UpdatePostView.as_view(), name='update_post'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name='logout'),
    path('logout_confirmation/', views.LogoutConfirmationView.as_view(), name='logout_confirmation'),
]