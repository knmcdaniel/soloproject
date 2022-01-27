from unicodedata import decimal
from django.db import models
import bcrypt, re

# Create your models here.

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}

        first_name = postData['first_name']
        if len(first_name) < 2:
            errors['first_name_not_valid'] = "Invalid First Name."

        last_name = postData['last_name']
        if len(last_name) < 2:
            errors['last_name_not_valid'] = "Invalid Last Name."

        password = postData['password']
        if len(password) < 2:
            errors['password_not_valid'] = "Invalid Password Length."

        confirm_password = postData['confirm_password']
        if password != confirm_password:
            errors['non_matching_passwords'] = "Your Passwords do not match"

        email = User.objects.filter(email=postData['email'])
        if email:
            errors['unique'] = "Email Taken"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = ("Invalid Email Address!")

        if len(errors) < 0:
            errors['create'] = ("User Created!")
        return errors
        
    def login_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])
        if not email:
            errors['creds'] = "Login Credentials Incorrect"
        else:
            logged_user = email[0]
            if not bcrypt.checkpw(postData['password'].encode(),logged_user.password.encode()):
                errors['creds'] = "Login Credentials Incorrect"
        login_errors = errors

        return login_errors

class ProductsManager(models.Manager):
    def product_validator(self, postData):
        errors = {}

        product_name = postData['product_name']
        if len(product_name) < 2:
            errors['product_name_not_valid'] = "Invalid Product Name"

        quantity = postData['quantity']
        if len(quantity) < 1:
            errors['no_inventory'] = "You must add a quantity."


        price_check = postData['price']
        if len(price_check) < 1:
            errors['price_not_valid'] = "Invalid Price"
        else:    
            price = round(float(postData['price']), 2)
            if price <= 0:
                errors['price_not_valid'] = "Invalid Price"
            sale_price_check = postData['sale_price']
            if len(sale_price_check) < 1:
                errors['price_not_valid'] = "Invalid Sale Price"
            else:
                sale_price = round(float(postData['sale_price']), 2)
                if sale_price <= 0:
                    errors['price_not_valid'] = "Invalid Sale Price"
                if sale_price > round(float(postData['price']), 2):
                    errors['sale_price_valid'] = "Invalid Sale Price"

        if len(errors) < 0:
            errors['create'] = ("Product Created!")

        return errors

class User(models.Model):
    #Object
    #id
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_vendor = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #relationships
    #One to many with products owned ----> products_owned
    #Many to many with products purchased ---> items_purchased

    #methods
    objects = UserManager()

    
class Products(models.Model):
    #Object
    #id
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    sale_price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    on_sale = models.CharField(max_length=50)
    amount_sold = models.IntegerField()
    #relationships
    vendor = models.ForeignKey(User, related_name="products_owned", on_delete = models.CASCADE)
    purchased_by = models.ManyToManyField(User, related_name="items_purchased")
    #methods
    objects = ProductsManager()

