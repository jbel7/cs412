from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form to create a new Post"""
    
    # Allow multiple image URLs, one per line
    image_urls = forms.CharField(
        required=False,
        label='Image URLs',
        help_text='Enter one image URL per line',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'https://example.com/image1.jpg\nhttps://example.com/image2.png'
        })
    )

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