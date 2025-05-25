from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'description', 'price', 'stock', 'is_available', 'category', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name', 'slug')
    list_filter = ('category', 'is_available')
    ordering = ('-created_at',)

admin.site.register(Product, ProductAdmin)