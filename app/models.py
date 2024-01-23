

from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name



class Sub_Category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    Availability = (('In stock','In stock'),('Out of stock','Out of stock'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=False,default='')
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE,null=False,default='')
    image = models.ImageField(upload_to='static/pimg')
    name = models.CharField(max_length=150)
    price = models.IntegerField() 
    Availability = models.CharField(choices=Availability, null=True,max_length=100)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.name
              
# signup page model

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email', error_messages={'exists': 'This Already Exists'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return email


        
class Contact_us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField() 


     



class Order(models.Model):
    image = models.ImageField(upload_to='static/context') 
    product = models.CharField(max_length=1000, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length=5)
    total = models.CharField(max_length=1000,default='')
    address = models.TextField()
    phone = models.CharField(max_length=11)
    pincode = models.CharField(max_length=11)
    # date = models.DateField(default=datetime.datetime.today)


    def __str__(self):
        return self.product
          
