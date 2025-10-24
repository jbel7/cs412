from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from django.urls import reverse
from django.db.models import Q
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ProfileLoginRequiredMixin(LoginRequiredMixin):
    """Custom mixin that requires login and provides helper to get the logged-in user's profile"""
    
    def get_login_url(self):
        """Redirect to login page"""
        return reverse('login')
    
    def get_profile(self):
        """Return the Profile associated with the logged-in user"""
        return Profile.objects.filter(user=self.request.user).first()


class ProfileListView(ListView):
    """Show all profiles - NO LOGIN REQUIRED"""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    """Show a single profile - NO LOGIN REQUIRED"""
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'


class PostDetailView(DetailView):
    """Show a single post - NO LOGIN REQUIRED"""
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'


class CreatePostView(ProfileLoginRequiredMixin, CreateView):
    """Create a new Post - LOGIN REQUIRED"""
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'
    
    def get_object(self):
        """Get the Profile of the logged-in user"""
        return self.get_profile()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context
    
    def form_valid(self, form):
        profile = self.get_profile()
        form.instance.profile = profile
        response = super().form_valid(form)
        
        files = self.request.FILES.getlist('files')
        for file in files:
            photo = Photo(post=self.object, image_file=file)
            photo.save()
        
        return response
    
    def get_success_url(self):
        return reverse('show_post', kwargs={'pk': self.object.pk})


class UpdateProfileView(ProfileLoginRequiredMixin, UpdateView):
    """Update an existing Profile or create a new one - LOGIN REQUIRED"""
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    
    def get_object(self):
        """Get the Profile of the logged-in user, or create one if it doesn't exist"""
        profile = self.get_profile()
        if not profile:
            # Create a new profile for the user
            profile = Profile.objects.create(
                user=self.request.user,
                username=self.request.user.username,
                display_name=self.request.user.get_full_name() or self.request.user.username,
                profile_image_url='https://via.placeholder.com/150x150/cccccc/666666?text=No+Image',
                bio_text=''
            )
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        context['profile'] = profile
        context['is_new_profile'] = not self.get_profile()  # Check if this is a new profile
        return context


class DeletePostView(ProfileLoginRequiredMixin, DeleteView):
    """Delete a Post - LOGIN REQUIRED"""
    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})


class UpdatePostView(ProfileLoginRequiredMixin, UpdateView):
    """Update a Post - LOGIN REQUIRED"""
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context
    
    def get_success_url(self):
        return reverse('show_post', kwargs={'pk': self.object.pk})


class ShowFollowersDetailView(DetailView):
    """Show followers - NO LOGIN REQUIRED"""
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'


class ShowFollowingDetailView(DetailView):
    """Show following - NO LOGIN REQUIRED"""
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'


class PostFeedListView(ProfileLoginRequiredMixin, DetailView):
    """Show the post feed - LOGIN REQUIRED"""
    model = Profile
    template_name = 'mini_insta/show_feed.html'
    
    
    def get_object(self):
        """Get the Profile of the logged-in user"""
        return self.get_profile()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['posts'] = profile.get_post_feed()
        return context


class SearchView(ProfileLoginRequiredMixin, ListView):
    """Search for Profiles and Posts - LOGIN REQUIRED"""
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'
    
    def get_object(self):
        """Get the Profile of the logged-in user"""
        return self.get_profile()
    
    def dispatch(self, request, *args, **kwargs):
        if 'query' not in self.request.GET:
            profile = self.get_profile()
            if not profile:
                # Redirect to profile creation if no profile exists
                return redirect('update_profile')
            return render(request, 'mini_insta/search.html', {'profile': profile})
        else:
            return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if query:
            return Post.objects.filter(caption__icontains=query).order_by('-timestamp')
        else:
            return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        if not profile:
            # Redirect to profile creation if no profile exists
            return redirect('update_profile')
        
        context['profile'] = profile
        
        query = self.request.GET.get('query', '')
        context['query'] = query
        context['posts'] = self.get_queryset()
        
        if query:
            context['profiles'] = Profile.objects.filter(
                Q(username__icontains=query) |
                Q(display_name__icontains=query) |
                Q(bio_text__icontains=query)
            ).order_by('username')
        else:
            context['profiles'] = Profile.objects.none()
        
        return context