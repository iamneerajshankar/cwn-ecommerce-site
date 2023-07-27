from itertools import product
from unicodedata import category

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from cart_app.models import Product
from cart_app.forms import UserRegistrationForm, CustomerProfileForm
from cart_app.models import Customer, Cart
from django.db.models import Q

from django.http import JsonResponse

# ec2828
class ProductView(View):
    def get(self, request):
        top_wear = Product.objects.filter(category='TW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')

        context = {
            'top_wear': top_wear,
            'mobiles': mobiles,
            'laptops': laptops
        }

        return render(request, 'cart_app/home.html', context)


class ProductDetailView(View):
    def get(self, request, pk):
        product_detail = Product.objects.get(pk=pk)
        context = {
            'product_detail': product_detail
        }
        return render(request, 'cart_app/product-detail.html', context)


def add_to_cart(request):
    user=request.user
    product_id = request.GET.get("prod_id")
    print(product_id)
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    print(product)
    return redirect('show-cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        cart_amount= 0.00
        shipping_amount = 70.00
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                temp_amount = (p.quantity) * (p.product.discounted_price)
                cart_amount +=temp_amount
                final_amount = cart_amount + shipping_amount
            return render(request, 'cart_app/add-to-cart.html', {'cart': cart, 'cart_amount':cart_amount ,'final_amount': final_amount})

def plus_to_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.quantity +=1
        cart_item.save()
        cart_amount= 0.00
        shipping_amount = 70.00
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            temp_amount = (p.quantity) * (p.product.discounted_price)
            cart_amount +=temp_amount
            final_amount = cart_amount + shipping_amount

        print("The cart amount is", cart_amount)
        data ={
            'quantity': cart_item.quantity,
            'cart_amount': cart_amount,
            'final_amount': final_amount
        }
        print(data)
        return JsonResponse(data)

def minus_from_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.quantity -=1
        cart_item.save()
        cart_amount= 0.00
        shipping_amount = 70.00
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            temp_amount = (p.quantity) * (p.product.discounted_price)
            cart_amount = cart_amount + temp_amount

        data ={
            'quantity': cart_item.quantity,
            'cart_amount': cart_amount,
            'final_amount': cart_amount + shipping_amount
        }
        print(data)
        return JsonResponse(data)

def remove_from_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart_item.delete()
        cart_amount= 0.00
        shipping_amount = 70.00
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        
        for p in cart_product:
            temp_amount = (p.quantity) * (p.product.discounted_price)
            cart_amount +=temp_amount
            final_amount = cart_amount + shipping_amount

        print("The cart amount is", cart_amount)
        data ={
            'cart_amount': cart_amount,
            'final_amount': final_amount
        }
        print(data)
        return JsonResponse(data)
def buy_now(request):
    return render(request, 'cart_app/buy-now.html')


class CustomerProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'cart_app/profile.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation!!! Profile Updated Successfully')
        return render(request, 'cart_app/profile.html', { 'form': form, 'active': 'btn-primary'})


def address(request):
    return render(request, 'cart_app/address.html')


def orders(request):
    return render(request, 'cart_app/orders.html')


def change_password(request):
    return render(request, 'cart_app/change-password.html')


def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == data == "Redmi" or data == "iPhone" or data == "Samsung" or data == "iQOO" or data == "One Plus":
        mobiles = Product.objects.filter(category="M").filter(brand=data)

    context = {
        'mobiles': mobiles
    }
    return render(request, 'cart_app/mobile.html', context)


# def customer_registration(request):
#   return render(request, 'cart_app/customer-registration.html')

class CustomerRegistrationView(View):
    @staticmethod
    def get(request):
        form = UserRegistrationForm()
        return render(request, 'cart_app/customer-registration.html', {'form': form})

    @staticmethod
    def post(request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'cart_app/customer-registration.html', {'form': form})


def checkout(request):
    return render(request, 'cart_app/checkout.html')
