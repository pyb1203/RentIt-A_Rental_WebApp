from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Product(models.Model):
    product_name      = models.CharField(max_length=250,null=False,blank=False)
    product_rate      = models.PositiveIntegerField(null=False,blank=False)
    product_date      = models.DateField(auto_now_add=True,null=False,blank=False)
    product_catagory  = models.CharField(max_length=100)
    product_image     = models.ImageField(upload_to='products/',null=False,blank=False)
    product_rules     = models.TextField(null=False,blank=False)
    location          = models.CharField(max_length=100)
    late_charge       = models.PositiveIntegerField(null=False,blank=False)
    user              = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class PendingProduct(models.Model):
    product_name      = models.CharField(max_length=250,null=False,blank=False)
    product_rate      = models.PositiveIntegerField(null=False,blank=False)
    product_date      = models.DateField(auto_now_add=True,null=False,blank=False)
    product_catagory = models.CharField(max_length=100)
    product_image     = models.ImageField(upload_to='products/',null=False,blank=False)
    product_rules     = models.TextField(null=False,blank=False)
    location          = models.CharField(max_length=100)
    late_charge       = models.PositiveIntegerField(null=False,blank=False)
    user              = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class Prebooking(models.Model):
    start_date = models.DateField(auto_now_add=False)
    end_date = models.DateField(auto_now_add=False)
    location = models.CharField(max_length=10)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
         return str(self.product_name)

class Booking(models.Model):
    prebooking = models.ForeignKey(Prebooking,on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.prebooking)

class FeedBack(models.Model):
      booking = models.ForeignKey(Booking,on_delete=models.CASCADE)
      text = models.CharField(max_length=5000)
      reviewed_at = models.DateTimeField(auto_now_add=True)

      def __str__(self):
          return str(self.booking)
