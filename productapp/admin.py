from django.contrib import admin
from .models import *
admin.site.register(Product)
admin.site.register(PendingProduct)
admin.site.register(Prebooking)
admin.site.register(Booking)
admin.site.register(FeedBack)
