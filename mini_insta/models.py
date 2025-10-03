from django.db import models
from django.utils import timezone
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
    
    class Meta:
        ordering = ['-timestamp']  # Most recent first


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')
    image_url = models.URLField(max_length=200)
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Photo for post {self.post.pk} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['timestamp']