
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Products
from django.db import models
from django.contrib import messages
import requests
import bcrypt


# Create your views here.

def index(request):
    context = {
        "products": Products.objects.all()
    }
    request.session.flush()
    return render(request, 'index.html', context)

def login_registration(request):
    return render(request, 'login_registration.html')

def new_product(request):
    if 'user_id' not in request.session:
        return redirect('/login_registration')
    context = {
        "user": User.objects.get(id= request.session['user_id']),
    }
    return render(request, 'new_product.html', context)

def main_landing(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id= request.session['user_id']),
        "products": Products.objects.all()
    }
    return render(request,'home.html', context)

def register(request):
    if request.method == "GET":
        return redirect('/login_registration')

    errors = User.objects.registration_validator(request.POST)

    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/login_registration')
    else:
        password = request.POST['password']

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash,
            is_vendor = request.POST['is_vendor']
        )
        request.session['user_id'] = new_user.id
    return redirect('/home')

def login(request):
    if request.method == "GET":
        return redirect('/login_registration')


    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/login_registration')
    else:
        logged_user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = logged_user.id
        return redirect('/home')


def account_main(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/login_registration')

    user = User.objects.get(id= user_id)

    context = {
        "user": User.objects.get(id= user_id),
        "products_purchased": Products.objects.filter(purchased_by=user),
        "products_owned": Products.objects.filter(vendor=user)
    }
    return render(request,'account.html', context)


def logout(request):
    request.session.flush()
    return redirect('/login_registration')

def create_product(request):
    if request.method == "GET":
        return redirect('/login_registration')

    errors = Products.objects.product_validator(request.POST)

    user = User.objects.get(id=request.session['user_id'])


    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/product/new')
    else:
        Products.objects.create(
            product_name = request.POST['product_name'],
            price = request.POST['price'],
            sale_price = request.POST['sale_price'],
            quantity = request.POST['quantity'],
            on_sale = request.POST['on_sale'],
            amount_sold = 0,
            vendor = user,
        )

    return redirect('/account/' +str(user.id)+'/view')

def view_product(request, product_id):
    if 'user_id' not in request.session:
        return redirect('/login_registration')

    user = User.objects.get(id=request.session['user_id'])
    product = Products.objects.get(id=product_id)
    buyers = product.purchased_by.all()

    context = {
        "user": user,
        "product": product,
        "buyers": buyers,
    }

    return render(request,'view_product.html', context)


def update(request, product_id):
    if request.method == "GET":
        return redirect('/login_registration')

    errors = Products.objects.product_validator(request.POST)

    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/product/'+ str(product_id)+'/edit')
    else:
        #product
        edit_product = Products.objects.get(id = product_id)
        #Change Value
        edit_product.product_name = request.POST['product_name']
        edit_product.price = request.POST['price']
        edit_product.sale_price = request.POST['sale_price']
        edit_product.quantity = request.POST['quantity']
        edit_product.on_sale = request.POST['on_sale']
        edit_product.updated_at = models.DateTimeField(auto_now=True)

        edit_product.save()

        context = {
        "user": User.objects.get(id=request.session['user_id']),
        "product": Products.objects.get(id=product_id)
        }


        return redirect('../../product/'+ str(product_id), context)

def destroy(request, product_id):

    destory_product= Products.objects.get(id = product_id)

    destory_product.delete()

    user = User.objects.get(id=request.session['user_id'])

    return redirect('/account/' +str(user.id)+'/view')

def edit(request, product_id):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    product = Products.objects.get(id=product_id)

    context = {
        "user": user,
        "product": product,
    }

    return render(request,'edit_product.html', context)

def buy_product(request, product_id):
    if 'user_id' not in request.session:
        return redirect('/login_registration')

    user = User.objects.get(id=request.session['user_id'])
    product = Products.objects.get(id=product_id)

    edit_product = Products.objects.get(id = product_id)
    edit_product.quantity -= 1
    edit_product.amount_sold += 1
    edit_product.purchased_by.add(user)

    edit_product.save()

    user.items_purchased.add(product)

    return redirect('/confirmation/' +str(product_id))

def confirmation(request, product_id):
    if 'user_id' not in request.session:
        return redirect('/login_registration')

    user = User.objects.get(id=request.session['user_id'])
    product = Products.objects.get(id=product_id)

    context = {
        "user": user,
        "product": product,
    }
    
    return render(request, 'confirmation.html', context)



