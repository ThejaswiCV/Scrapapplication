from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Sum
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404

from django.views.generic import View,CreateView,FormView,UpdateView,TemplateView,DetailView,ListView

from django.urls import reverse

from django.contrib import messages

from scrapapp.forms import RegistrationForm,LoginForm,UserProfileForm,CategoryForm,ScrapForm,BidsForm

from django.contrib.auth import authenticate,login,logout

from scrapapp.models import UserProfile,Scraps,Category,WishList,Bids

from django.utils.decorators import method_decorator

# Create your views here.

def signin_required(fn):
   def wrapper(request,*args,**kwargs):
      if not request.user.is_authenticated:
         messages.error(request,"Sign in required")
         return redirect('sign-in')
      else:
         return fn(request,*args,**kwargs)
   return wrapper

   
class SignUpView(CreateView):
   template_name="register.html"
   form_class=RegistrationForm
   
   def get_success_url(self):
      return reverse('sign-in')
   
   
class signInView(FormView): 
   template_name="login.html"
   form_class=LoginForm
   
   def post(self,request,*args,**kwargs):
      form=LoginForm(request.POST)
      if form.is_valid():
         uname=form.cleaned_data.get("username")
         pwd=form.cleaned_data.get("password")
         user_object=authenticate(request,username=uname,password=pwd)
         if user_object:
            login(request,user_object)
            print("success")
            return redirect('index')     
      else:
            print("failed")
            return render(request,"login.html",{"form":form})


@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
   def get(self,request,*args,**kwargs):
      logout(request)
      return redirect('sign-in')


@method_decorator(signin_required,name="dispatch")
class IndexView(ListView):
   template_name="index.html" 
   model=Scraps
   context_object_name="data" 
   
   def get_queryset(self):
      #display all scraps except the one added by loggined user
      qs=Scraps.objects.all().exclude(user=self.request.user)
      return qs
  
         
@method_decorator(signin_required,name="dispatch")         
class ProfileUpdateView(UpdateView):
   template_name="profile_update.html"
   form_class= UserProfileForm
   model= UserProfile
   print('updated profile')
   

   
   def get_success_url(self):
      return reverse("index")   
 
   
@method_decorator(signin_required,name="dispatch")   
class ProfileDeatilView(DetailView):
   template_name="profile_detail.html"
   model=UserProfile
   context_object_name="data"
   
   def get_context_data(self, **kwargs: Any):
      context =super().get_context_data(**kwargs)
      user_items = Scraps.objects.filter(user=self.request.user)
      user_bids = Bids.objects.filter(user=self.request.user)
      
      context['user_items'] = user_items
      context['user_bids'] = user_bids
   
      return context
 
   
@method_decorator(signin_required,name="dispatch")          
class ScrapaddView(CreateView):
   template_name="scrap_add.html"
   form_class=ScrapForm
   model=Scraps
   context_object_name="data"
   
   def form_valid(self, form):
      form.instance.user=self.request.user
      return super().form_valid(form)
   
   def get_success_url(self):
      return reverse('index')
   
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all() 
        return context

     
@method_decorator(signin_required,name="dispatch")     
class ScrapDetailView(DetailView):
   template_name="scrap_detail.html"
   model=Scraps
   context_object_name="data"      
         
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scrap=self.get_object()
        
        bid_item=scrap.scrap_bid.all()
        context['wishlist_toggle_url'] = reverse('wishlist_toggle', args=[self.object.id])
        context['bid_item']=bid_item
        context['bid_url']=reverse('bid',args=[self.object.id])
        context['user'] = self.request.user
        return context      


@method_decorator(signin_required,name="dispatch")
class ScrapUpdateView(UpdateView):
   template_name="scrap_update.html"
   form_class=ScrapForm
   model=Scraps
   print('scrap updated')  
   
   def get_success_url(self):
      return reverse('index')   
 
     
@method_decorator(signin_required,name="dispatch")
class ScrapDeleteView(View):
   def get(self,request,*args,**kwargs):
      id=kwargs.get("pk")
      Scraps.objects.get(id=id).delete()
      return redirect("index")
 
     
@method_decorator(signin_required,name="dispatch")
class WishlistView(View):
    def get(self, request, scraps_id):
        scraps = get_object_or_404(Scraps, pk=scraps_id)
        
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            wishlist_items = user_profile.wishlists.all()            
            total_price = wishlist_items.aggregate(total_price=Sum('price'))['total_price'] or 0
            
            return render(request, 'cart.html',{
                'scraps':scraps,
                'wishlist_items': wishlist_items,
                'total_price': total_price,
                
            })
        
       
    
    def post(self, request, scraps_id):
        scraps = get_object_or_404(Scraps, pk=scraps_id)
        
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            if scraps not in user_profile.wishlists.all():
               
                user_profile.wishlists.add(scraps)
        
        return HttpResponseRedirect(reverse('wishlist_toggle', kwargs={'scraps_id': scraps_id}))

   
@method_decorator(signin_required,name="dispatch")   
class WishlistDeleteView(View):
    def get(self, request, pk):
        scrap = get_object_or_404(Scraps, pk=pk)

        if request.user.is_authenticated:
            user_profile = request.user.profile
            user_profile.wishlists.remove(scrap)

            return redirect('index') 


@method_decorator(signin_required,name="dispatch") 
class BidsView(CreateView):
   template_name="scrap_detail.html"
   form_class=BidsForm

   
   def form_valid(self, form):
      id = self.kwargs.get("pk")
      scrap_object = Scraps.objects.get(id=id)
      form.instance.user = self.request.user
      form.instance.scrap = scrap_object 
      return super().form_valid(form)
   
      
   def get_success_url(self) :
      # scraps_id=self.kwargs.get('pk')
      # return reverse("scrap_details",kwargs={'pk':self.kwargs['scraps_id']})
      return reverse("index")
 
   
@method_decorator(signin_required,name="dispatch")
class BidsDeleteView(View):
   def get(self,request,*args,**kwargs):
      id=kwargs.get("pk")
      Bids.objects.get(id=id).delete()
      return redirect("index")
  
  
@method_decorator(signin_required,name="dispatch")         
class BidRequestView(View):
      def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        scrap = Scraps.objects.get(id=id)
        bids = scrap.scrap_bid.all()
        return render(request,'bid_request.html',{'scrap': scrap,
                                                  'bids': bids,})        
      
      def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        action=request.POST.get("action")
        if action=="accept":
            Bids.objects.filter(id=id).update(status="Accepted")
            messages.success(request, 'Bid request accepted!')
        elif action=="reject":
            Bids.objects.filter(id=id).update(status="Rejected")
            Bids.objects.filter(id=id).delete()
            messages.error(request, 'Bid request rejected')
        return redirect("index")
   

class CheckoutView(ListView):
   template_name="checkout.html" 
   model=WishList
   

class CategoryView(View):
   def get(self,request,*args,**kwargs):
      categories = Category.objects.all()
      return render(request, 'index.html', {'categories': categories})
   