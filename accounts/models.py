from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Users(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_businessOwner = models.BooleanField(default = False)


    USERNAME_FIELD = 'username'

    