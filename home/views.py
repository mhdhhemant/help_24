from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from accounts.models import Users
from django.core.mail import send_mail 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from  .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.views.generic.base import View
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
                                    Description=Adescription,image='pics/'+Image)
        business.save()
        return redirect('/')
    
    else:
        return render(request,'list.html')


def listings(request):
    business1=Business_List.objects.all()
    return render(request, 'listings.html',{'business1':business1})


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
                    # user = UserRegister(firstname=firstname, lastname=lastname, email=email, password=password,
                    #                     username=username
                    #                     )

                    # user.save()
                elif(role == 'business'):
                    user1 = Users.objects.create_user(first_name=firstname, last_name=lastname, email=email, password=password,
                                        username=username,is_businessOwner=True
                                        )
                    # user = Business_detail(firstname=firstname, lastname=lastname, email=email, password=password,
                    #                     username=username
                    #                     )
                    # user.save()
                
                user1.is_active=False
                user1.save();

                current_site=get_current_site(request)

                subject='Activate your Account'
                message=render_to_string('activate_account.html',{
                    'user':user1,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user1.pk)),
                    'token': account_activation_token.make_token(user1),
                })
                send_mail(
                    subject,
                    message,
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



class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            #uid = force_text(urlsafe_base64_decode(uidb64))
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, user.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request)
            messages.success(request, ('Your account have been confirmed.'))
            return render(request,'home.html')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('/Thanks')
