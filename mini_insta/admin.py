from django.contrib import admin
from .models import Profile
from .models import Post
from .models import Photo
# Register your models here.

#Registers model with admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'display_name', 'join_date']
    list_filter = ['join_date']
    search_fields = ['username', 'display_name']
    ordering = ['username']

    def post_count(self, obj):
        return obj.get_all_posts().count()
    post_count.short_description = 'Posts'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['profile', 'caption_preview', 'timestamp', 'photo_count']
    list_filter = ['timestamp', 'profile']
    search_fields = ['caption', 'profile__username']
    ordering = ['-timestamp']
    
    def caption_preview(self, obj):
        return obj.caption[:50] + '...' if len(obj.caption) > 50 else obj.caption
    caption_preview.short_description = 'Caption'
    
    def photo_count(self, obj):
        return obj.get_all_photos().count()
    photo_count.short_description = 'Photos'


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['post', 'image_url_preview', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['post__caption', 'post__profile__username']
    ordering = ['-timestamp']
    
    def image_url_preview(self, obj):
        return obj.image_url[:60] + '...' if len(obj.image_url) > 60 else obj.image_url
    image_url_preview.short_description = 'Image URL'