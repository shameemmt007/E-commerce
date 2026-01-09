from django.shortcuts import render,redirect,HttpResponse
from .forms import RegForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Product,category,OrderItem,Order,UserProfile
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.shortcuts import get_object_or_404
from .forms import ProfileForm
# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required

def Register(request):
    if request.method=='POST':
        regform = RegForm(request.POST)
        if regform.is_valid():
            usr = regform.save()
            UserProfile.objects.create(user=usr)
            messages.success(request,'user has been registered')
            return redirect(loginpage)
    else:
        regform = RegForm()
    return render(request,'register.html',{'regform':regform})

def loginpage(request):
    if request.method=='POST':
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request,username=usern,password=passw)
        if user:
            login(request,user)
            messages.success(request,'user has been loged ')
        else:
            print('invalid')
    return render(request,'login.html')

def logoutpage(request):
    logout(request)
    messages.success(request,'user has been logout')
    return redirect(loginpage)
@login_required(login_url='login_page')
def allproduct(request):
    products=Product.objects.all()
    return render(request,'allproducts.html',{'products':products})

def productdetails(request,pid):
    productd=Product.objects.get(id=pid)
    return render(request,'product.html',{'productd':productd})


@login_required(login_url='login_page')
def catagorypage(request):
    catagory = category.objects.all()
    return render(request,'catagory.html',{'catagory':catagory})

def catgryprodt(request,cpid):
    procat = Product.objects.filter(categorys=cpid)
    return render(request,'catgryprodt.html',{'procat':procat})

def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            print('product added')
            return redirect(allproduct)
    else:
        form = ProductForm()
    return render(request,'create.html',{'form':form})

def updateproduct(request,upid):
    pro = Product.objects.get(id=upid)
    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES,instance=pro)
        if form.is_valid():
            form.save()
            return redirect(allproduct)
    else:
        form = ProductForm(instance=pro)
    return render(request,'updatepro.html',{'form':form})

def deleteproduct(request,did):
    pro = Product.objects.get(id=did)
    if request.method == "POST":
        pro.delete()
        return redirect(allproduct)
    return render(request,'delete.html',{'pro':pro})




def order_details(request,order_id):
    order = get_object_or_404(Order)
    order_items = order.orderitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in order_items)
    return render(request,'useritem.html')








# @login_required
# def view_cart(request):
#     cart = Cart.objects.filter(user=request.user).first()
#     cart_items = CartItem.objects.filter(cart=cart) if cart else []
#     total_price = sum(item.product.price * item.quantity for item in cart_items)
#     return render(request,'cart.html',{'cart_items': cart_items,'total_price':total_price})

# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product,id=product_id)
#     cart,created = Cart.objects.get_or_create(user=request.user)
#     item ,created = CartItem.objects.get_or_create(cart=cart, product=product)

#     if request.method == 'POST':
#         quantity = int(request.POST.get("quantity",1))
#         if quantity <= 0:
#             quantity = 1
#         if not created:
#             item.quantity += quantity
#         else:
#             item.quantity = quantity
#         item.save()
#     return redirect(view_cart)

# def update_cart(request,item_id):
#     item = get_object_or_404(CartItem,id=item_id,cart__user=request.user)

#     if request.method == "POST":
#         quantity = int(request.POST.get("quantity",1))
#         if quantity > 0:
#             item.quantity = quantity
#             item.save()
#         else:
#             item.delete()
#     return redirect(view_cart)
 
# @login_required
# def remove_from_cart(request,item_id):
#     item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
#     item.delete()
#     return redirect(view_cart)



def add_to_cart(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    cart = request.session.get('cart',{})
    quantity = int(request.POST.get("quantity",1))

    if quantity <= 0:
        quantity = 1
    
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    
    else:
        cart[str(product_id)] = quantity

    request.session['cart'] = cart

    return redirect(view_cart)


def view_cart(request):
    cart = request.session.get('cart',{})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total = product.price * quantity
        total_price += total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total
        })

    return render(request,'cart.html',{'cart_items':cart_items,'total_price':total_price})

def update_cart(request,product_id):
    cart = request.session.get('cart',{})
    if request.method == 'POST':
        quantity = int(request.POST.get("quantity",1))
        if quantity <= 0:
            if str(product_id) in cart:
                del cart[str(product_id)]
        else:
            cart[str(product_id)] = quantity

    request.session['cart'] = cart
    return redirect(view_cart)

def remove_from_cart(request,product_id):
    cart = request.session.get('cart',{})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session['cart'] = cart
    return redirect(view_cart)


@login_required
def checkout(request):
    if request.method != 'POST':
        return redirect(view_cart)
    
    cart = request.session.get('cart',{})

    if not cart:
        return redirect(view_cart)
    
    order = Order.objects.create(user=request.user)

    for product_id, quantity in cart.items():
        OrderItem.objects.create(
            order=order,
            product_id=product_id,
            quantity=quantity

        )

    request.session['cart'] = {}
    request.session.modified = True

    return redirect(order_detail,order_id=order.id)

@login_required
def order_detail(request,order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request,'order_detail.html',{'order':order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request,'order_list.html',{'orders':orders})



@staff_member_required
def manage_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, "manage_orders.html",{"orders":orders})

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get("status")
        if status in dict(order.STATUS_CHOICES).keys():
            order.status = status
            order.save()
        return redirect(manage_orders)
    return render(request, "update_order_status.html",{"order":order})

@staff_member_required
def delete_orders(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return redirect(manage_orders)



@login_required
def profile_page(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request,'profile.html',{'profile':profile})

def edit_profile(request):
    pro = UserProfile.objects.get(user=request.user)
    if request.method=='POST':
        form = ProfileForm(request.POST,request.FILES,instance=pro)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm(instance=pro)
    return render(request,'editprofile.html',{'form':form})



