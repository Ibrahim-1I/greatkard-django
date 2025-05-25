from django.contrib import admin

# Register your models here.

from .models import Category



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('Category_name', 'slug', 'description', 'cat_img')
    prepopulated_fields = {'slug': ('Category_name',)}
    search_fields = ('Category_name', 'slug')
    list_filter = ('Category_name',)

admin.site.register(Category, CategoryAdmin)