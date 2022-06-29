from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,redirect
from .models import *
from .urls import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from twilio.rest import Client


# Your Account SID from twilio.com/console
account_sid = "AC12d8b2af4b9398c3b740110607ceda38"
# Your Auth Token from twilio.com/console
auth_token  = "5df044cdc239bc2435d7220a8a50a0e8"

def productview(request):
    obj = Product.objects.all()
    return render(request,'products/products_new.html',{'obj': obj})

@login_required(login_url='login')
def addproducts(request):
        if request.method == 'POST':
            product_name = request.POST['product_name']
            product_rate = request.POST['product_rate']
            product_catagory=request.POST['drop1']
            product_image = request.FILES['product_image']
            product_rules = request.POST['product_rules']
            location = request.POST['location']
            late_charge = request.POST['late_charge']
            current_user = request.user
            PendingProduct.objects.create(product_name = product_name, product_rate=product_rate,product_catagory=product_catagory,product_image=product_image,product_rules=product_rules,location=location,late_charge=late_charge,user = current_user )
            return render(request, 'products/addproducts.html')
        else:
            print("not posted")
            return render(request, 'products/addproducts.html')

@login_required(login_url='login')
def productdetails(request,id):
    obj = Product.objects.get(pk=id)
    return render(request,'products/viewproducts1.html',{'obj':obj})


def catagories(request):
    return render(request,'Base/base.html')

@staff_member_required
def pending(request):
    obj = PendingProduct.objects.all()
    if request.method == "POST":

        value = request.POST['123']
        print(value)
        action = value[0]
        product_id = value[1] + value[2] +value[3]
        spc = PendingProduct.objects.filter(id = product_id)
        print(action)
        if action == '0':
          for i in spc:
            product_name = i.product_name
            product_date = i.product_date
            product_rate = i.product_rate
            product_catagory = i.product_catagory
            product_image = i.product_image
            product_rules = i.product_rules
            location = i.location
            late_charge = i.late_charge
            user = i.user
            print(product_name,product_rate)
            Product.objects.create(product_name = product_name, product_rate = product_rate, product_date =product_date,product_catagory=product_catagory,product_image=product_image,product_rules=product_rules,location=location,late_charge=late_charge,user=user)
            print("Created")
            spc.delete()
            return render(request,'admin/pending.html',{'obj':obj})
        else:
            a = PendingProduct.objects.filter(id = product_id)
            print("Deleted")
            a.delete()
            return render(request, 'admin/pending.html',{'obj':obj})
    else:
        return render (request,'admin/pending.html',{'obj':obj})
@login_required(login_url='login')
def userproducts(request):
        current_user = request.user
        obj = Product.objects.filter(user = current_user)
        
      
        if request.method == 'POST':
             value = request.POST['123']
             action = value[0]
             product_id = value[1] + value[2] 
             
             print(value)
             if action == '0':
                return render(request, 'user/myproducts.html',{'obj':obj})
                
             else:
                a = Product.objects.filter(id = product_id)
                print("Deleted")
                a.delete()
                return render(request, 'user/myproducts.html',{'obj':obj})
        else:
             return render(request, 'user/myproducts.html',{'obj':obj})
            
@login_required(login_url='login')
def prebooking(request):

    current_user = request.user

    if request.method == 'POST':
        trip_start = request.POST['start']
        trip_end   = request.POST['end']
        location   = request.POST['location']
        product_id = request.POST['product_id']
        start = trip_start.split('-')
        s_year = int(start[0])
        s_month = int(start[1])
        s_day = int(start[2])
        end = trip_end.split('-')
        e_year = int(end[0])
        e_month = int(end[1])
        e_day = int(end[2])
        start_date = datetime.date(s_year, s_month, s_day)
        end_date = datetime.date(e_year,e_month,e_day)
        product_name = Product.objects.filter(id=product_id).first()


        if product_name.user != current_user:
            a = Prebooking.objects.create(start_date=start_date, end_date=end_date, location=location,
                                          product_name=product_name, user=current_user)
            a.save()

            return redirect('mybid')


        else:

            mess = "Easy Man! This is Your Product"
            return redirect('products')

    else:

       return render(request,'user/myproducts.html')
@login_required(login_url='login')
def mybid(request):
    current_user = request.user
    obj = Prebooking.objects.filter(user=current_user)
    if request.method == 'POST':
         product_id = request.POST['123']
         a = Prebooking.objects.filter(id = product_id)
         a.delete()
         return render(request, 'user/mybid.html', {'obj': obj})
    else:
        return render(request, 'user/mybid.html', {'obj': obj})
@login_required(login_url='login')
def rent_request(request):
    current_user = request.user
    obj1 = Product.objects.filter(user=current_user)
    obj = []
    for i in obj1:
        obj.append(Prebooking.objects.all().filter(product_name=i))
    if request.method == "POST":
        value = request.POST['123']
        action = value[0]
        id = value[1]+value[2]
        if action == '0':
            pre = Prebooking.objects.filter(id=id).first()
            if Booking.objects.filter(prebooking = pre):
               print("sorry")
            else:
               Booking.objects.create(prebooking = pre)
               client = Client(account_sid, auth_token)
               message = client.messages.create(
                   to="+916367769281",
                   from_="+19707143090",
                   body="Hello {} Accepted Your Request. Check Your Dashboard. BY RentIt".format(current_user)
               )


            return render(request, 'user/rent_request.html',{'obj':obj})
        else:
            a = Prebooking.objects.filter(id=id)
            a.delete()



            return render(request, 'user/rent_request.html',{'obj':obj})

    else:

            return render(request, 'user/rent_request.html',{'obj':obj})
@login_required(login_url='login')
def accepted_offer(request):
    current_user = request.user
    obj1 = Product.objects.filter(user=current_user)
    obj = []
    object = []
    for i in obj1:
        obj.append(Prebooking.objects.all().filter(product_name=i))
    print(obj)
    for i in obj:
        for j in i:

            if Booking.objects.filter(prebooking=j):
                object.append(j)
                print(object)
            else:
                print("sorry")
    return render(request, 'user/acc_off.html',{'object':object})
@login_required(login_url='login')
def hired_products(request):
    obj = []
    current_user = request.user
    po = Prebooking.objects.filter(user = current_user)
    for i in po:
        if Booking.objects.filter(prebooking = i).exists():
            obj.append(i)
        else:
            print("sorry")
    return render(request,'user/hired_products.html',{'obj':obj})
@login_required(login_url='login')
def feedback(request):
    if request.method == "POST":
        value = request.POST['123']
        print(value)
    return render(request,'user/Feedback.html')
