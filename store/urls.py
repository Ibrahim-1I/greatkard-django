
from django.urls import path
from django.conf.urls.static import static

from greadkard import settings 
from . import views
from .views import product_detail, store

from .views import store
urlpatterns = [
    path('', store, name='store'),
    path('category/<slug:category_slug>/', store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
    path('search/', views.search, name='search'), 
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)