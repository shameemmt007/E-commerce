from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *
urlpatterns = [
    path('register',Register,name='register'),
    path('login',loginpage,name='login_page'),
    path('logout',logoutpage,name='logout_page'),
    path('allproducts',allproduct,name='all_products'),
    path('prodetails/<int:pid>',productdetails,name='product_details'),
    path('catagorypage',catagorypage,name='store_homepage'),
    path('catryprodt/<int:cpid>',catgryprodt,name='catgry_prodt'),
    path('create',create,name='create'),
    path('update/<int:upid>',updateproduct,name='update_product'),
    path('delete/<int:did>',deleteproduct,name='delete_pro'),
    # path('addtocart/<int:product_id>',add_to_cart,name='addtocart'),
    # path('cart',view_cart,name='viewcart'),
    # path('remove/<int:item_id>',remove_from_cart,name='remove_from_cart'),
    # path('updat/<int:item_id>',update_cart,name='update_cart'),
    path('profile',profile_page,name='profile_page'),
    path('editprofile',edit_profile,name='edit_profile'),
    path('addtocart/<int:product_id>',add_to_cart,name='addtocart'),
    path('cart',view_cart,name='viewcart'),
    path('remove/<int:product_id>',remove_from_cart,name='remove_from_cart'),
    path('updat/<int:product_id>',update_cart,name='update_cart'),

    path('order/<int:order_id>/',order_detail,name='order_detail'),
    path('orders/',order_list,name='order_list'),
    path('checkout/',checkout,name='checkout'),

    path('morders/',manage_orders,name='manage_orders'),
    path('uorder/<int:order_id>/',update_order_status,name='update_order_status'),
    path('dorders/<int:order_id>/',delete_orders,name='delete_order')
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)