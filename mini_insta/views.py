from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo, Follow, Like, Comment
from django.urls import reverse
from django.db.models import Q
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm, CreateCommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse

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


class LogoutConfirmationView(TemplateView):
    """Show logout confirmation page"""
    template_name = 'mini_insta/logged_out.html'


class CreateProfileView(CreateView):
    """Create a new Profile and User account - NO LOGIN REQUIRED"""
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'
    
    def get_context_data(self, **kwargs):
        """Add UserCreationForm to context"""
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        """Handle both User and Profile creation"""
        # Create User from UserCreationForm
        user_form = UserCreationForm(self.request.POST)
        if not user_form.is_valid():
            # If user form is invalid, re-render with errors
            return self.render_to_response(self.get_context_data(form=form, user_form=user_form))
        
        # Save the User
        user = user_form.save()
        
        # Log the user in
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Attach the User to the Profile
        form.instance.user = user
        
        # Save the Profile
        response = super().form_valid(form)
        
        # Redirect to the user's profile page
        return redirect('show_profile', pk=self.object.pk)


class FollowProfileView(ProfileLoginRequiredMixin, TemplateView):
    """Follow a profile - LOGIN REQUIRED"""
    
    def dispatch(self, request, *args, **kwargs):
        # Get the profile to follow
        profile_to_follow = get_object_or_404(Profile, pk=kwargs['pk'])
        current_user_profile = self.get_profile()
        
        # Prevent following yourself
        if current_user_profile == profile_to_follow:
            return redirect('show_profile', pk=profile_to_follow.pk)
        
        # Create follow relationship
        follow, created = Follow.objects.get_or_create(
            profile=profile_to_follow,
            follower_profile=current_user_profile
        )
        
        # Redirect back to the profile page
        return redirect('show_profile', pk=profile_to_follow.pk)


class UnfollowProfileView(ProfileLoginRequiredMixin, TemplateView):
    """Unfollow a profile - LOGIN REQUIRED"""
    
    def dispatch(self, request, *args, **kwargs):
        # Get the profile to unfollow
        profile_to_unfollow = get_object_or_404(Profile, pk=kwargs['pk'])
        current_user_profile = self.get_profile()
        
        # Prevent unfollowing yourself
        if current_user_profile == profile_to_unfollow:
            return redirect('show_profile', pk=profile_to_unfollow.pk)
        
        # Delete follow relationship
        Follow.objects.filter(
            profile=profile_to_unfollow,
            follower_profile=current_user_profile
        ).delete()
        
        # Redirect back to the profile page
        return redirect('show_profile', pk=profile_to_unfollow.pk)


class LikePostView(ProfileLoginRequiredMixin, TemplateView):
    """Like a post - LOGIN REQUIRED"""
    
    def dispatch(self, request, *args, **kwargs):
        # Get the post to like
        post = get_object_or_404(Post, pk=kwargs['pk'])
        current_user_profile = self.get_profile()
        
        # Prevent liking your own post
        if current_user_profile == post.profile:
            return redirect('show_post', pk=post.pk)
        
        # Create like relationship
        like, created = Like.objects.get_or_create(
            post=post,
            profile=current_user_profile
        )
        
        # Redirect back to the post page
        return redirect('show_post', pk=post.pk)


class UnlikePostView(ProfileLoginRequiredMixin, TemplateView):
    """Unlike a post - LOGIN REQUIRED"""
    
    def dispatch(self, request, *args, **kwargs):
        # Get the post to unlike
        post = get_object_or_404(Post, pk=kwargs['pk'])
        current_user_profile = self.get_profile()
        
        # Prevent unliking your own post
        if current_user_profile == post.profile:
            return redirect('show_post', pk=post.pk)
        
        # Delete like relationship
        Like.objects.filter(
            post=post,
            profile=current_user_profile
        ).delete()
        
        # Redirect back to the post page
        return redirect('show_post', pk=post.pk)


class CreateCommentView(ProfileLoginRequiredMixin, CreateView):
    """Create a new Comment on a Post - LOGIN REQUIRED"""
    model = Comment
    form_class = CreateCommentForm
    template_name = 'mini_insta/create_comment_form.html'
    
    def get_object(self):
        """Get the Post to comment on"""
        return get_object_or_404(Post, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        context['profile'] = self.get_profile()
        return context
    
    def form_valid(self, form):
        # Get the post and current user's profile
        post = self.get_object()
        profile = self.get_profile()
        
        # Attach the post and profile to the comment
        form.instance.post = post
        form.instance.profile = profile
        
        # Save the comment
        form.save()
        
        # Redirect back to the post page
        return redirect('show_post', pk=post.pk)