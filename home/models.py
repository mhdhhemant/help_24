from django.db import models

# Create your models here.
class Trending(models.Model):
    category= models.CharField(max_length=200)
    img=models.ImageField(upload_to='pics')
    address=models.TextField()
    title=models.CharField(max_length=200)

class FindBusiness(models.Model):
    title= models.CharField(max_length=200)
    img=models.ImageField(upload_to='pics1')


class UserRegister(models.Model):
    firstname=models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    password=models.CharField(max_length=200)
    username=models.CharField(max_length=100)