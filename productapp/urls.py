from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',productview, name="products"),
    path('addproducts/',addproducts, name ="addproducts"),
    path('products/<int:id>/', productdetails, name='productdetails'),
    path('super-user-pending/',pending, name='pending'),
    path('myproducts/',userproducts ,name='myproducts'),
    path('prebooking/', prebooking,name= 'prebooking'),
    path('mybid/',mybid,name='mybid'),
    path('offer/',rent_request,name='rent_request'),
    path('accepted-offer', accepted_offer, name='acc_off'),
    path('hired_products', hired_products, name='hired_products'),
    path('feedback', feedback , name ='feedback')


]

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

