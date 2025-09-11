# file: quotes/views.py

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

quotes = [
    "I don't care that they stole my idea . . I care that they don't have any of their own",
    "The present is theirs; the future, for which I really worked, is mine.", 
    "One must be sane to think clearly, but one can think deeply and be quite insane.",
    "Be alone, that is the secret of invention; be alone, that is when ideas are born.",
    "If your hate could be turned into electricity, it would light up the whole world.",
    "I do not think you can name many great inventions that have been made by married men."
]

images = [
    "https://upload.wikimedia.org/wikipedia/commons/7/79/Tesla_circa_1890.jpeg",
    "https://cdn.britannica.com/19/187119-050-C555ADE1/Nikola-Tesla-Publicity-photo-laboratory-Colorado-Springs-December-1899.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/d/d4/N.Tesla.JPG",
    "https://www.ocduk.org/wp-content/uploads/2018/05/Nikola-Tesla-OCDUK.jpg",
    "https://npr.brightspotcdn.com/dims4/default/1218f68/2147483647/strip/true/crop/475x608+0+0/resize/880x1126!/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Flegacy%2Fsites%2Fkwgs%2Ffiles%2F201307%2Fnikola-tesla-with-lamp.jpg"
       # Replace with actual image URL
]


# Create your views here.

def home(request):
    # pick a random Tesla image
    image = random.choice(images)
    return render(request, "quotes/home.html", {"image": image})
    
def quote(request):
    """View for the main page - displays one random quote and image"""
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    
    context = {
        'quote': selected_quote,
        'image': selected_image
    }
    
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    """View to show all quotes and images"""
    context = {
        'quotes': quotes,
        'images': images
    }

    return render(request, 'quotes/show_all.html', context)

def about(request):
    """View for the about page"""
    context = {
        'person_name': 'Nikola Tesla',  # Replace with actual name
        'person_bio': 'Nikola Tesla (1856–1943) was a brilliant inventor and visionary who transformed the modern world. Born in what is now Croatia, he came to the U.S. and introduced alternating current (AC), making it possible to send electricity across cities and continents. Tesla’s inventions, like the Tesla coil and the induction motor, laid the groundwork for radio, wireless communication, and even robotics. Though he often lived in poverty, his imagination stretched far beyond his time—dreaming of wireless power, global communication, and technologies that still inspire scientists today.',
        'creator_name': 'Jed Belsany',  # Replace with your name
        'creator_info': 'Boston University(2027) Computer Science and Economics major'
    }
    
    return render(request, 'quotes/about.html', context)
