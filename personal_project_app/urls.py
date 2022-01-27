from django.urls import path     
from . import views


urlpatterns = [
    path('', views.index),
    path('login_registration', views.login_registration),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('home', views.main_landing),
    path('confirmation/<int:product_id>', views.confirmation),
    path('account/<int:user_id>/view', views.account_main),
    path('product/new', views.new_product),
    path('product/create', views.create_product),
    path('product/<int:product_id>/edit', views.edit),
    path('product/<int:product_id>/update', views.update),
    path('product/<int:product_id>/destory', views.destroy),
    path('product/<int:product_id>', views.view_product),
    path('product/<int:product_id>/buy', views.buy_product),
] 