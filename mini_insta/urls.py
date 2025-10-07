# URL pattern for mini_insta app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='show_post'),
    path('profile/<int:pk>/create_post', views.CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/update', views.UpdateProfileView.as_view(), name='update_profile'),
]