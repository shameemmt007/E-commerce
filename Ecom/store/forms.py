from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Product, UserProfile

class RegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','price','image','description','categorys']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']