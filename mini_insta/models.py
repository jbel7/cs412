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