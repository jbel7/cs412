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
    list_display = ['post', 'has_file', 'has_url', 'timestamp']
    list_filter = ['timestamp']
    ordering = ['-timestamp']
    
    def has_file(self, obj):
        return bool(obj.image_file)
    has_file.boolean = True
    has_file.short_description = 'Has File'
    
    def has_url(self, obj):
        return bool(obj.image_url)
    has_url.boolean = True
    has_url.short_description = 'Has URL'