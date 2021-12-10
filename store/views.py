from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login,logout
from .forms import CreateUserForm


from .models import *

from django.contrib import messages


import json
import datetime
from store.models import *

from .utils import cartData,guestOrder
# Create your views here.

def store(request):
     data = cartData(request)
     cartItems = data['cartItems']    
     products = Product.objects.all()
     context = {'products': products, 'cartItems': cartItems }
     return render(request, 'store/store.html', context)

def cart(request):
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     
     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']

     context = {'items':items, 'order':order, 'cartItems':cartItems}
     return render(request, 'store/checkout.html', context)

def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Action:',action)
     print('productId:',productId)


     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order,created = Order.objects.get_or_create(customer=customer,complete=False) 
     orderItem,created = OrderItem.objects.get_or_create(order=order, product=product)


     if action =='add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)
     orderItem.save()

     if orderItem.quantity<=0:
          orderItem.delete()
     return JsonResponse('Item was added', safe=False)



def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer,complete = False)
          
     else:
          customer,order = guestOrder(request,data)

     total = float(data['form']['total'])
     order.transaction_id = transaction_id

     if total == float(order.get_cart_total):
          order.complete = True
     order.save()

     if order.shipping == True:
          ShippingAddress.objects.create(
               customer = customer,
               order = order,
               address = data['shipping']['address'],
               city = data['shipping']['city'],
               state = data['shipping']['state'],
               zipcode = data['shipping']['zipcode']
          )
     return JsonResponse('Payment complete!', safe=False)     


def search(request):
     if request.method=='POST':
          data = cartData(request)
          cartItems = data['cartItems']  
          query = request.POST['search']
          filterproduct = Product.objects.filter(name__icontains=query)
          context = {'filterproduct': filterproduct, 'cartItems' : cartItems, 'query':query}
          return render(request, "store/search.html",context)

     
def electronics(request):
     data = cartData(request)

     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     products = Product.objects.filter(category=1)
     context = {'items':items, 'order':order, 'cartItems':cartItems, 'products': products}
     return render(request,'store/electronics.html', context)


def men(request):
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     products = Product.objects.filter(category=3)
     context = {'items':items, 'order':order, 'cartItems':cartItems, 'products': products}
     return render(request,'store/men.html', context)


def women(request):
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     products = Product.objects.filter(category=4)
     context = {'items':items, 'order':order, 'cartItems':cartItems, 'products': products}
     return render(request,'store/women.html', context)


def kids(request):
     data = cartData(request)
     cartItems = data['cartItems']
     order = data['order']
     items = data['items']
     products = Product.objects.filter(category=5)
     context = {'items':items, 'order':order, 'cartItems':cartItems, 'products': products}
     return render(request,'store/kids.html', context)


def productView(request, pk):
    product = Product.objects.get(name=pk)
    data = cartData(request)
    order = data['order']
    cartItems = data['cartItems'] 
    context = {'product': product, 'cartItems' : cartItems, 'order' : order}
    return render(request, 'store/view.html', context) 


def signup(request):
     data = cartData(request)
     cartItems = data['cartItems']    
     order = data['order']
     products = Product.objects.all()
     context = { 'cartItems': cartItems, 'orer': order,'products' : products}
     form = CreateUserForm()
     if request.method=='POST':
          form = CreateUserForm(request.POST)
          if form.is_valid():
               form.save()
               messages.success(request,"Hooray!!! Your are now Registered...")
               return redirect('store')

     context = {'form': form}
     return render(request, 'store/signup.html',context)


def loginfunc(request):
     data = cartData(request)
     cartItems = data['cartItems']    
     order = data['order']

     if request.method=='POST':
          username = request.POST.get('loginusername')
          password = request.POST.get('loginpassword')

          user = authenticate(request,username=username, password=password)
          
          if user is not None:
               login(request, user)
               messages.success(request, "Hooray!!! You are logged in..")
               return redirect('store')
          else:
               messages.error(request,"You entered incorrect username or password!!!")
               return redirect('store')

     context = { 'cartItems': cartItems, 'order': order}
     return render(request, 'store/login.html',context )

def logoutUser(request):
     logout(request)
     messages.error(request,"You are logged out")
     return redirect('store')

def forgot(request):
     return render(request, 'store/forgot_password.html')
          
def about(request):
     data = cartData(request)
     cartItems = data['cartItems']    
     order = data['order']
     context = { 'cartItems': cartItems, 'order': order}
     return render(request, 'store/aboutus.html',context)

def contact(request):
     data = cartData(request)
     cartItems = data['cartItems']    
     order = data['order']
     context = { 'cartItems': cartItems, 'order': order}

     return render(request, 'store/contactus.html',context)

def getinfo(request):
     if request.method=='POST':
          name = request.POST.get('fullname')
          eml = request.POST.get('email')
          msg = request.POST.get('message')

          info = Contact.objects.create(name=name,email=eml,message=msg)
          info.save()
          messages.success(request, "Message sent")
          return redirect('store')

