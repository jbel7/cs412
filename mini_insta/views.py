from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from django.urls import reverse
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm

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

# Adds the detail view to posts on each profile
class PostDetailView(DetailView):
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    """View to create a new Post"""
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def get_context_data(self, **kwargs):
        """Add the Profile to the context data"""
        context = super().get_context_data(**kwargs)
        # Get the profile from the URL parameter
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context
    
    def form_valid(self, form):
        """Handle the form submission to create Post and Photo"""
        # Get the profile from the URL parameter
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        
        # Attach the profile to the post before saving
        form.instance.profile = profile
        
        # Save the post (this will call super().form_valid())
        response = super().form_valid(form)
        
        # Handle uploaded files
        files = self.request.FILES.getlist('files')
        for file in files:
            photo = Photo(
                post=self.object,
                image_file=file
            )
            photo.save()
        
        return response
    
    def get_success_url(self):
        """Redirect to the post detail page after successful creation"""
        return reverse('show_post', kwargs={'pk': self.object.pk})

class UpdateProfileView(UpdateView):
    """View to update an existing Profile"""
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    """View to delete a Post"""
    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Add the Profile to the context data"""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
        """Redirect to the profile page after successful deletion"""
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class UpdatePostView(UpdateView):
    """View to update a Post"""
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """Add the Profile to the context data"""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
        """Redirect to the post detail page after successful update"""
        return reverse('show_post', kwargs={'pk': self.object.pk})