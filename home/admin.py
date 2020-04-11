from django.contrib import admin
from .models import Trending,FindBusiness,UserRegister,Business_detail
# Register your models here.

admin.site.register(Trending)
admin.site.register(FindBusiness)
admin.site.register(Business_detail)
admin.site.register(UserRegister)
