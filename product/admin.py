from django.contrib import admin
from .models import Variant, Product, ProductImage, ProductVariant,ProductVariantPrice
# Register your models here.

ls=[Variant,Product, ProductImage, ProductVariant, ProductVariantPrice]
admin.site.register(ls)
