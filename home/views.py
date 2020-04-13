from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from accounts.models import Users
from django.core.mail import send_mail 
# Create your views here.

from .models import FindBusiness, Trending, UserRegister, Business_detail,Business_List


def index(request):
    finds = FindBusiness.objects.all()
    news = Trending.objects.all()

    return render(request, 'index.html', {'finds': finds, 'news': news})


def about(request):
    return render(request, 'about.html')


def blog(request):
    return render(request, 'blog.html')


def blogsingle(request):
    return render(request, 'blog-single.html')


def contact(request):
    return render(request, 'contact.html')

def list(request):
    if request.method=="POST":
        pin=request.POST['pincode']
        Bname=request.POST['businessname']
        category=request.POST['category']
        Bphone=request.POST['phone']
        Address=request.POST['address']
        Landmark=request.POST['landmark']
        Waddress=request.POST['webaddress']
        Email=request.POST['email']
        Image=request.POST['image']
        Adescription=request.POST['description']

        business=Business_List(business_name=Bname,pincode=pin,email=Email,category=category,
                                   phone=Bphone,address=Address,landmark=Landmark,website=Waddress,
                                    Description=Adescription,image=Image)
        business.save()
        return redirect('/')
    
    else:
        return render(request,'list.html')


def listings(request):
    return render(request, 'listings.html',{'numbers':range(10)})


def listingssingle(request):
    return render(request, 'listings-single.html')


def login(request):
    
    if request.method=="POST":
        use=request.POST['username']
        pass1=request.POST['password']
        
        user=auth.authenticate(username=use,password=pass1)
        
        if user is not None:
            auth.login(request,user)
            
            return redirect('/')
        else:
            messages.info(request,"*Invalid Credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')



def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['cpassword']
        username = request.POST['username']
        role = request.POST['role']
        if password == password1:
            if Users.objects.filter(username=username).exists():
                messages.info(request, '*Username taken')
                return redirect('register')
            elif Users.objects.filter(email=email).exists():
                messages.info(request, '*Email taken')
                return redirect('register')
            else:
                if(role== 'user'):
                    user1 = Users.objects.create_user(first_name=firstname, last_name=lastname, email=email, password=password,
                                        username=username,is_user=True
                                        )
                    user = UserRegister(firstname=firstname, lastname=lastname, email=email, password=password,
                                        username=username
                                        )

                    user.save()
                elif(role == 'business'):
                    user1 = Users.objects.create_user(first_name=firstname, last_name=lastname, email=email, password=password,
                                        username=username,is_businessOwner=True
                                        )
                    user = Business_detail(firstname=firstname, lastname=lastname, email=email, password=password,
                                        username=username
                                        )
                    user.save()
                
                user1.save();
                send_mail(
                    'Confirmation',
                    'This mail is intended to use for confirming your account.',
                    'EMAIL_HOST_USER',
                    [email],
                    fail_silently=False

                )

        else:
            messages.info(request, '*Password not matching')
            return redirect('register')
        return redirect('login')


    else:
        return render(request, 'register.html')



