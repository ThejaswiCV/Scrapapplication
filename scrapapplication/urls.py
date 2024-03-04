"""
URL configuration for scrapapplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from scrapapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register',views.SignUpView.as_view(),name='sign-up'),
    path('login',views.signInView.as_view(),name="sign-in"),
    path('logout',views.SignOutView.as_view(),name='sign-out'),
    path('index',views.IndexView.as_view(),name='index'),
    path('profile/<int:pk>/change',views.ProfileUpdateView.as_view(),name="profile_update"),
    path('profile/<int:pk>',views.ProfileDeatilView.as_view(),name='profile_detail'),
    path('scrap',views.ScrapaddView.as_view(),name='scrap_add'),
    path('scrap/<int:pk>',views.ScrapDetailView.as_view(),name='scrap_details'),
    path('scrap/<int:pk>/change',views.ScrapUpdateView.as_view(),name='scrap_update'),
    path('scrap/<int:pk>/delete',views.ScrapDeleteView.as_view(),name="scrap_delete"),
    path('wishlist/<int:scraps_id>',views.WishlistView.as_view(),name="wishlist_toggle"),
    path('scrap/<int:pk>/bid/add',views.BidsView.as_view(),name="bid"),
    path('bids/<int:pk>/delete',views.BidsDeleteView.as_view(),name='bids_delete'),
    path('wishlist/delete/<int:pk>',views.WishlistDeleteView.as_view(),name='wishlist_delete'),
    path("bids/<int:pk>",views.BidRequestView.as_view(),name="bids_request"),
    path("checkout",views.CheckoutView.as_view(),name="checkout"),
    path("category",views.CategoryView.as_view(),name="category_detail")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
