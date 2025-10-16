from django.contrib import admin
from .models import Profile
from .models import Post
from .models import Photo
from .models import Follow
from .models import Comment
from .models import Like
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

    def follower_count(self, obj):
        return obj.get_num_followers()
    follower_count.short_description = 'Followers'


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

    def comment_count(self, obj):
        return obj.get_all_comments().count()
    comment_count.short_description = 'Comments'

    def like_count(self, obj):
        return obj.get_likes().count()
    like_count.short_description = 'Likes'

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


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower_profile', 'profile', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['profile__username', 'follower_profile__username']
    ordering = ['-timestamp']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['profile', 'post', 'text_preview', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['text', 'profile__username']
    ordering = ['-timestamp']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comment'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['profile', 'post', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['profile__username']
    ordering = ['-timestamp']