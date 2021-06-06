from django import forms
from django.contrib.auth.models import User
from FoodApp.models import Food
from django.db.models import fields
from django.db.models.enums import Choices
from django.db.models.fields import FloatField
from django.db.models.fields.files import ImageField 
from FoodApp.models import Food,UserProfile

class FoodForm(forms.ModelForm):
    category=[('veg','vegetarian'),('Non-veg','Non-vegetarian')]

    name=forms.CharField(widget=forms.TextInput(attrs={'class':'c1'}))
    price=forms.FloatField(widget=forms.TextInput(attrs={'class':'c1'}))
    quantity=forms.IntegerField(widget=forms.TextInput(attrs={'class':'c1'}))
    type=forms.CharField(widget=forms.TextInput(attrs={'class':'c1'}))
    category=forms.ChoiceField(choices=category)
    image=forms.ImageField()
    class Meta:
        model=Food
        fields='__all__'
class SignUpForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    role=[('customer','customer','admin','ADMIN')]
    Role=forms.ChoiceField(choices=role,widget=forms.RadioSelect)
    class Meta:
        model=User
        fields=['username','password','email','first_name','last_name']

class Profileform(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['location','number']
    
    
    
    
    
    
