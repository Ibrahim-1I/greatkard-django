from django.contrib import admin
from .models import Product
from .models import Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'description', 'price', 'stock', 'is_available', 'category', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('product_name',)}
    search_fields = ('product_name', 'slug')
    list_filter = ('category', 'is_available')
    ordering = ('-created_at',)

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter= ('product', 'variation_category', 'variation_value')
   

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)