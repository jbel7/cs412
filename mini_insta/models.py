from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.

# Display for profile page
class Profile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    profile_image_url = models.URLField(max_length=200)
    bio_text = models.TextField(max_length=500)
    join_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.username} ({self.display_name})"

    def get_all_posts(self):
        """Return all Posts for this Profile, ordered by timestamp (newest first)"""
        return Post.objects.filter(profile=self).order_by('-timestamp')

    def get_absolute_url(self):
        """Return the URL to display this Profile"""
        return reverse('show_profile', kwargs={'pk': self.pk})

    def get_followers(self):
        """Return a list of Profiles who follow this profile"""
        # Get all Follow objects where this profile is being followed
        follows = Follow.objects.filter(profile=self)
        # Return list of the follower profiles
        return [follow.follower_profile for follow in follows]
    
    def get_num_followers(self):
        """Return the count of followers"""
        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        """Return a list of Profiles that this profile follows"""
        # Get all Follow objects where this profile is the follower
        follows = Follow.objects.filter(follower_profile=self)
        # Return list of the profiles being followed
        return [follow.profile for follow in follows]
    
    def get_num_following(self):
        """Return the count of profiles being followed"""
        return Follow.objects.filter(follower_profile=self).count()

    def get_post_feed(self):
        """Return all Posts from profiles that this profile follows, ordered by timestamp"""
        following = self.get_following()
        
        """Get all posts from those profiles, ordered by most recent first"""
        posts = Post.objects.filter(profile__in=following).order_by('-timestamp')
        
        return posts
    
    class Meta:
        ordering = ['username']

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(max_length=2000, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Post by {self.profile.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    def get_all_photos(self):
        """Return all Photos for this Post, ordered by timestamp"""
        return Photo.objects.filter(post=self).order_by('timestamp')

    def get_absolute_url(self):
        """Return the URL to display this Post"""
        return reverse('show_post', kwargs={'pk': self.pk})

    def get_all_comments(self):
        """Return all Comments for this Post, ordered by timestamp"""
        return Comment.objects.filter(post=self).order_by('-timestamp')
    
    def get_likes(self):
        """Return all Likes for this Post"""
        return Like.objects.filter(post=self)
    
    
    class Meta:
        ordering = ['-timestamp']  # Most recent first


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField(max_length=200, blank=True)
    image_file = models.ImageField(upload_to='photos/', blank=True) #New: for uploaded files
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        if self.image_file:
            return f"Photo (file) for post {self.post.pk}"
        else:
            return f"Photo (URL) for post {self.post.pk}"
    
    def get_image_url(self):
        """Return the URL for this image, whether from image_url or image_file"""
        if self.image_file:
            return self.image_file.url
        else:
            return self.image_url

    class Meta:
        ordering = ['timestamp']


class Follow(models.Model):
    """Represents a follow relationship between two profiles"""
    profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='followers'  # The profile being followed
    )
    follower_profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='following'  # The profile doing the following
    )
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"
    
    class Meta:
        unique_together = ('profile', 'follower_profile')  # Prevent duplicate follows


class Comment(models.Model):
    """Represents a comment on a post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Comment by {self.profile.username} on post {self.post.pk}"
    
    class Meta:
        ordering = ['-timestamp']


class Like(models.Model):
    """Represents a like on a post"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.profile.username} likes post {self.post.pk}"
    
    class Meta:
        unique_together = ('post', 'profile')  # One like per user per post