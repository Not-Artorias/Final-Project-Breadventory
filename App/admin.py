from django.contrib import admin
from .models import Ingredient, Product, SaleItem, Sale

admin.site.register(Ingredient)
admin.site.register(Product)
admin.site.register(SaleItem)
admin.site.register(Sale)
