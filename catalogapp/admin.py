from django.contrib import admin
from catalogapp.models import Categorie, Product, Cart, Review

model_list =[
    Categorie,
    Product,
    Cart,
    Review,  
]
admin.site.register(model_list)