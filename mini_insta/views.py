from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from django.urls import reverse
from django.db.models import Q
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

class ShowFollowersDetailView(DetailView):
    """View to show all followers of a profile"""
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'


class ShowFollowingDetailView(DetailView):
    """View to show all profiles that this profile follows"""
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(DetailView):
    """View to show the post feed for a profile"""
    model = Profile
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        """Get the post feed for this profile"""
        context['posts'] = self.object.get_post_feed()
        return context

class SearchView(ListView):
    """View to search for Profiles and Posts"""
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'
    
    def dispatch(self, request, *args, **kwargs):
        """Handle the request, show form or results"""
        """Checks if query parameter exists"""
        if 'query' not in self.request.GET:
            """No query yet, show the search form"""
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            return render(request, 'mini_insta/search.html', {'profile': profile})
        else:
            """Query exists, continue with ListView to show results"""
            return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """Return Posts that match the search query"""
        query = self.request.GET.get('query', '')
        
        if query:
            """Search for posts where caption contains the query (case-insensitive)"""
            return Post.objects.filter(caption__icontains=query).order_by('-timestamp')
        else:
            return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        """Add profile, query, and matching profiles to context"""
        context = super().get_context_data(**kwargs)
        
        """Get the profile doing the search"""
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        
        """Get the search query"""
        query = self.request.GET.get('query', '')
        context['query'] = query
        
        """Get posts (already from get_queryset)"""
        context['posts'] = self.get_queryset()
        
        """Search for matching profiles"""
        if query:
            context['profiles'] = Profile.objects.filter(
                Q(username__icontains=query) |
                Q(display_name__icontains=query) |
                Q(bio_text__icontains=query)
            ).order_by('username')
        else:
            context['profiles'] = Profile.objects.none()
        
        return context