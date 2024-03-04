from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from scrapapp.models import UserProfile,Category,Scraps,WishList,Bids

class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","password1","password2"]
        
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()      
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile    
        exclude=('user',)  
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=["name"]     
        
class ScrapForm(forms.ModelForm):
    class Meta:
        model=Scraps
        exclude=('user','created_date')  
        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "condition":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "place":forms.TextInput(attrs={"class":"form-control"})
        }    
        
class CartForm(forms.ModelForm):
    class Meta:
        model=WishList
        exclude=('user',)
        
class BidsForm(forms.ModelForm):
    class Meta:
        model=Bids
        fields=['amount']   
        
        
         