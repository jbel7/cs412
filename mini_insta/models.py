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
    
    class Meta:
        ordering = ['username']
