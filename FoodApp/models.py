from os import name
from django.db import models
from django.contrib.auth.models import Group,Permission,User
import datetime
# Create your models here.
class Food(models.Model):
    category=[('veg','vegetarian'),('non-veg','non-vegetarian')]
    name=models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.IntegerField()
    type = models.CharField(max_length=30)
    category = models.CharField(choices=category,max_length=30)
    image = models.ImageField(upload_to='media',default='')
    class Meta:
        db_table='foodDB'
#admin,create= Group.objects.get_or_create(name='admin')
#customer,create1=Group.objects.get_or_create(name='customer')

#class Cart(models.Model):
 #   custemail=models.EmailField(max_length=50)
  #  itemquantity=models.IntegerField()
  
  
  

   # total=models.DecimalField(max_digits=10,decimal_places=0)

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    location=models.CharField(max_length=50)
    number=models.CharField(max_length=10)
    class Meta:
        db_table='userProfile'


admin,create=Group.objects.get_or_create(name='admin')
customer,create1=Group.objects.get_or_create(name='customer')

class Cart(models.Model):
    currentuser=models.ForeignKey(User,on_delete=models.CASCADE)
    itemquantity=models.IntegerField(default=1)
    fid=models.ForeignKey(Food,on_delete=models.CASCADE)
    total=models.FloatField()
    class Meta:
        db_table='cart'

class OrderSummery1(models.Model):
    statusChoices = [('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel')]
    date = models.DateTimeField(auto_now_add=True)
    totalamount = models.FloatField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=19, choices=statusChoices, default='Pending')

    class Meta:
        db_table="orderSummery"


class Orders(models.Model):
    order=models.ForeignKey(OrderSummery1,on_delete=models.CASCADE)
    food=models.ForeignKey(Food,on_delete=models.CASCADE)
    total=models.IntegerField()
    foodQuant= models.IntegerField()

    class Meta:
        db_table="Orders"
