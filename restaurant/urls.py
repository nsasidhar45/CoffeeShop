# restaurant/urls.py
from django.urls import path
from . import views


urlpatterns = [
    # User functions
    path('menu/', views.view_menu, name='view_menu'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('cart/', views.view_cart, name='cart'), 
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'), 
    path('view_orders/', views.view_orders, name='view_orders'), 


    # Manager functions
    path('add_item/', views.add_item, name='add_item'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('view_all_orders/', views.view_all_orders, name='view_all_orders'),
    path('view_users/', views.view_users, name='view_users'),
    path('view_all_items/', views.view_all_items, name='view_all_items'), 
    path('index/', views.index, name='index'), 
    path('manager/', views.manager, name='manager'),
    path('update_status/<int:order_id>/', views.update_order_status, name='update_status'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('edit_order/<int:order_id>/', views.edit_order, name='edit_order'),

    
]
