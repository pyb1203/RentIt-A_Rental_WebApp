from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
import os
from twilio.rest import Client
from random import randint


# Your Account SID from twilio.com/console
account_sid = "AC12d8b2af4b9398c3b740110607ceda38"
# Your Auth Token from twilio.com/console
auth_token  = "5df044cdc239bc2435d7220a8a50a0e8"

def GenerateRandomNumber():
    number = randint(1000, 9999)
    return number
Vcode1 = GenerateRandomNumber()
VCode = Vcode1

def sign_up(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 =request.POST['password1']

        if password == password1:
            if User.objects.filter(username = username).exists():
                messages.warning(request,"username taken")
                return render(request,'accounts/userregistration.html')
            elif User.objects.filter(email =email).exists():
                messages.warning(request,"email taken")
                return render(request,'accounts/userregistration.html')
            else:
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                       to="+916367769281", 
                       from_="+19707143090",
                       body="Hello {}, Your verification number  {}".format(username,VCode)
                       )

                context={
                    'username':username,
                    'email':email,
                    'password':password,
                }
                return render(request,'accounts/verify.html',context)         
        else:
            messages.warning(request,"Password not matched")
            return render(request,'accounts/userregistration.html')
    else:
        return render(request,'accounts/userregistration.html')
    
    
def register(request):         
       return render(request,'accounts/verify.html')


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password =password)
        if user is not None:
            auth.login(request,user)
            return redirect('addproducts')
        else:
            return render(request,'accounts/userlogin.html')
    else:
        return render(request,'accounts/userlogin.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


def verify(request):
    if request.method == 'POST':
        one = request.POST['one']
        two = request.POST['two']
        three = request.POST['three']
        four = request.POST['four']
        five = request.POST['five']
        five = five.split(',')
        username = five[0]
        email = five[1]
        password = five[2]
        value = int(one+two+three+four)
        if VCode == value:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request,"Account Created")
            return render(request, 'accounts/userlogin.html')
        else:
            return render(request, 'accounts/userregistration.html')
        return render(request,'accounts/verify.html')
    else:
        return render(request,'accounts/verify.html')


    

