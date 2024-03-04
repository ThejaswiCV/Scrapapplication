from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)    
    
    def __str__(self):
        return self.name


class Scraps(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_scrap")
    name=models.CharField(max_length=200)
    condition=models.CharField(max_length=200)
    picture=models.ImageField(upload_to="scrappics",null=True)
    price=models.CharField(max_length=200)
    place=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="scrap_cat")
    created_date=models.DateTimeField(auto_now_add=True)
    options=(
        ("Available","Available"),
        ("Soldout","Soldout")
        
    )
    status=models.CharField(max_length=200,choices=options,default="Available")
    
    def __str__(self) :
        return self.name


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)
    profile_picture=models.ImageField(upload_to="profilepics",null=True,blank=True)
    wishlists = models.ManyToManyField(Scraps, related_name='wishlisted_by', blank=True)
    
    def __str__(self) :
        return self.user.username
    
def create_profile(sender,created,instance,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('profile object created')    
    
post_save.connect(create_profile,sender=User) 
    

class Bids(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_bid")
    scrap=models.ForeignKey(Scraps,on_delete=models.CASCADE,related_name="scrap_bid")    
    amount=models.PositiveIntegerField()
    options=(
        ("rejected","rejected"),
        ("pending","pending"),
        ("accepted","accepted")
    )
    status=models.CharField(max_length=200,choices=options,default="pending")
    
    def __str__(self):
        return self.user.username

    
class WishList(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_wish")
    scrap=models.ManyToManyField(Scraps)
    created_date=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.scrap.name
    
       
    
class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_review")  
    scrap=models.ForeignKey(Scraps,on_delete=models.CASCADE,related_name="scrap_review") 
    comment=models.CharField(max_length=200)
    rating=models.CharField(max_length=200) 
    
    def __str__(self):
        return self.comment
      