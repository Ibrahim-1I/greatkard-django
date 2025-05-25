from django.db import models
from django.urls import reverse  

# Create your models here.
class Category(models.Model):
    Category_name = models.CharField(max_length=50 , unique=True)
    # Removed invalid ForeignKey to undefined 'category'
    # If you want a self-referential ForeignKey, use 'self' as shown below:
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True , max_length=250)
    cat_img = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['Category_name']

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])


    def __str__(self):
        return self.Category_name