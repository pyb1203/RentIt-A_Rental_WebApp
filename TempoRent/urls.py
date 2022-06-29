from typing import List, Any

from django.contrib import admin
from django.urls import path,include

urlpatterns=[
    path('admin/', admin.site.urls),
    path('', include('productapp.urls')),
    path('account/', include('accountsapp.urls')),
    path('accounts/', include('allauth.urls')),

]
