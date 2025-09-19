from django.shortcuts import render
from django.http import HttpResponse
import random
import time
from datetime import datetime, timedelta

def main(request):
    """View for the main restaurant page."""
    return render(request, 'restaurant/main.html')

def order(request):
    """View for the ordering page with daily special."""
    # Daily specials for Crown Chicken and Gyro
    daily_specials = [
        {'name': 'Chicken Kabob with Yellow Rice and Salad', 'price': 13.99, 'description': 'Tender marinated chicken kabobs, grilled to perfection and served over fragrant yellow rice with our creamy signature white sauce. Served with a fresh side salad'},
        {'name': '3 Piece Chicken with Fries', 'price': 11.99, 'description': 'Crispy golden fried chicken, served with a side of seasoned fries'},
        {'name': 'Lamb Gyro, Chicken Kabob, a Mix with Yellow Rice and Salad', 'price': 25.96, 'description': 'A flavorful combination of lamb gyro and tender chicken kabob, served over yellow rice with fresh garden salad'},
        {'name': 'Tres Leches Cake', 'price': 6.99, 'description': 'Moist sponge cake soaked in three sweet milks, topped with whipped cream for a rich and decadent finish'},
    ]
    
    # Select random daily special
    daily_special = random.choice(daily_specials)
    
    context = {
        'daily_special': daily_special
    }
    
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    """View to process order submission and display confirmation."""
    if request.method == 'POST':
        # Crown Chicken and Gyro menu items with prices
        menu_items = {
            'chicken_kabob': {'name': 'Chicken Kabob with Yellow Rice Only', 'price': 10.99},
            'mozzarella_sticks': {'name': '6 piece Mozzarella sticks', 'price': 6.99},
            'lamb_gyro': {'name': 'Lamb Gyro with Yellow Rice Only', 'price': 10.99},
            'beef_patty': {'name': 'Beef Patty', 'price': 3.99},
            'daily_special': {'name': request.POST.get('daily_special_name', ''), 'price': float(request.POST.get('daily_special_price', 0))}
        }
        
        # Process ordered items
        ordered_items = []
        total_price = 0
        
        # Check regular menu items
        for item_key, item_info in menu_items.items():
            if item_key in request.POST:
                item_detail = {
                    'name': item_info['name'],
                    'price': item_info['price']
                }
                
                # Handle special options for Crown Chicken and Gyro items
                if item_key == 'chicken_kabob':
                    extras = request.POST.getlist('kabob_extras')
                    if extras:
                        item_detail['extras'] = extras
                        # Add cost per extra
                        item_detail['price'] += len(extras) * 2.00
                
                elif item_key == 'lamb_gyro':
                    extras = request.POST.getlist('gyro_extras')
                    if extras:
                        item_detail['extras'] = extras
                        # Add cost per extra
                        item_detail['price'] += len(extras) * 1.50
                
                elif item_key == 'beef_patty':
                    extras = request.POST.getlist('patty_extras')
                    if extras:
                        item_detail['extras'] = extras
                        # Add cost per extra
                        item_detail['price'] += len(extras) * 0.50
                
                ordered_items.append(item_detail)
                total_price += item_detail['price']
        
        # Customer information
        customer_info = {
            'name': request.POST.get('customer_name', ''),
            'phone': request.POST.get('customer_phone', ''),
            'email': request.POST.get('customer_email', ''),
            'special_instructions': request.POST.get('special_instructions', '')
        }
        
        # Calculate ready time (30-60 minutes from now)
        current_time = datetime.now()
        ready_minutes = random.randint(30, 60)
        ready_time = current_time + timedelta(minutes=ready_minutes)
        
        context = {
            'ordered_items': ordered_items,
            'customer_info': customer_info,
            'total_price': round(total_price, 2),
            'ready_time': ready_time,
            'order_number': random.randint(100, 999)  # Simple order number
        }
        
        return render(request, 'restaurant/confirmation.html', context)
    
    else:
        # If not POST request, redirect to order page
        return render(request, 'restaurant/order.html')