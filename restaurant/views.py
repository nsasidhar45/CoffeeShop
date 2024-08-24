from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item, Cart, Order, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages


#Authentication
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if the username or email is already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken.')
            return redirect('register')
        
        # Create the user
        user = User.objects.create(username=username, email=email, password=make_password(password))
        user.save()
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')
    
    return render(request, 'user/register.html')

#user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'user/login.html')

#logout
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

#USER FUNCTIONS
#view orders
@login_required
def view_orders(request):
    if request.user.is_authenticated:
        # Fetch orders related to the currently logged-in user
        user_orders = Order.objects.filter(user=request.user)

        # Pass the orders to the template
        return render(request, 'user/user_orders.html', {'orders': user_orders})
    else:
        # Handle the case when the user is not logged in
        # Redirect to login page 
        return redirect(user_login)
    

#view menu
def view_menu(request):
    categories = Item.objects.values_list('category', flat=True).distinct()

    selected_category = request.GET.get('category')

    if selected_category:
        items = Item.objects.filter(category=selected_category)
    else:
        items = Item.objects.all()

    return render(request, 'user/menu.html', {'categories': categories, 'items': items, 'selected_category': selected_category})


#add to cart
@login_required
def add_to_cart(request, item_id):
    item = Item.objects.get(pk=item_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect(view_menu)

#view cart
@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.item.price for item in cart_items)
    return render(request, 'user/cart.html', {'cart_items': cart_items, 'total_price': total_price})

#place orders
@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum([item.item.price * item.quantity for item in cart_items])
    order = Order.objects.create(user=request.user, total_price=total_price)
    order.items.set([item.item for item in cart_items])
    cart_items.delete()
    return render(request, 'user/order.html', {'order': order})


#MANAGER FUNCTIONS
#Add new items
@staff_member_required
def add_item(request):
     if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']
        category = request.POST['category']
        subcategory = request.POST['subcategory']
        image = request.FILES['image'] 
        Item.objects.create(name=name, price=price, category=category, subcategory=subcategory, image=image)
        return redirect('view_all_items')
     
     return render(request, 'manager/add_item.html')

#View orders
@staff_member_required
def view_all_orders(request):
    orders = Order.objects.all()
    return render(request, 'manager/view_orders.html', {'orders': orders})

#update orders



#View users
@staff_member_required
def view_users(request):
    users = User.objects.all()
    return render(request, 'manager/view_users.html', {'users': users})

#Edit existing items
@staff_member_required
def edit_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == 'POST':
        item.name = request.POST['name']
        item.price = request.POST['price']
        item.category = request.POST['category']
        item.subcategory = request.POST['subcategory']
        item.save()
        return redirect('view_all_items')

    return render(request, 'manager/edit_item.html', {'item': item})

#delete item
@staff_member_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    
    if request.method == 'POST':
        item.delete()
        return redirect('view_all_items')
    
    return render(request, 'manager/confirm_delete.html', {'item': item})

#edit order
def edit_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = order.items.all()

    if request.method == 'POST':
        for order_item in order_items:
            item_id = order_item.item.id
            new_quantity = request.POST.get(f'quantity_{item_id}')
            order_item.quantity = int(new_quantity)
            order_item.save()

        # Update the total price based on the new quantities
        order_items = Order.items.all()
        total_price = sum(item.quantity * item.item.price for item in order_items)
        order.total_price = total_price
        order.save()

        return redirect('view_orders')

    return render(request, 'manager/edit_orders.html', {'order': order, 'order_items': order_items})

#view all items
@staff_member_required
def view_all_items(request):
    items = Item.objects.all()
    return render(request, 'manager/view_all_items.html', {'items': items})

#index
def index(request):
    items = Item.objects.all()
    return render(request, 'index.html', {'items': items})

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = 'delivered'
    order.save()
    return redirect('view_all_orders')

@staff_member_required
def manager(request):
    return redirect('view_all_orders')