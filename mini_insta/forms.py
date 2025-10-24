from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form to create a new Post"""
    
    class Meta:
        model = Post
        fields = ['caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a caption for your post...'
            }),
        }
        labels = {
            'caption': 'Caption',
        }


class UpdateProfileForm(forms.ModelForm):
    """Form to update an existing Profile"""
    
    class Meta:
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']
        widgets = {
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your display name'
            }),
            'bio_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us about yourself...'
            }),
            'profile_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/your-image.jpg'
            }),
        }
        labels = {
            'display_name': 'Display Name',
            'bio_text': 'Bio Text',
            'profile_image_url': 'Profile Image URL',
        }

class UpdatePostForm(forms.ModelForm):
    """Form to update an existing Post"""
    
    class Meta:
        model = Post
        fields = ['caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Update your caption...'
            }),
        }
        labels = {
            'caption': 'Caption',
        }


class CreateProfileForm(forms.ModelForm):
    """Form to create a new Profile"""
    
    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a unique username'
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your display name'
            }),
            'bio_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us about yourself...'
            }),
            'profile_image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/your-image.jpg'
            }),
        }
        labels = {
            'username': 'Username',
            'display_name': 'Display Name',
            'bio_text': 'Bio Text',
            'profile_image_url': 'Profile Image URL',
        }


class CreateCommentForm(forms.ModelForm):
    """Form to create a new Comment"""
    
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Write a comment...'
            }),
        }
        labels = {
            'text': 'Comment',
        }