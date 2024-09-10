"""
URL configuration for GoogleMyBusiness project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from reviews.views import google_login,fetch_reviews,review_list,add_reply

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
   
    path('api/google-login/', google_login, name='google_login'),
    path('fetch-reviews/', fetch_reviews, name='fetch_reviews'),
    path('reviews/', review_list, name='review_list'),
    path('reviews/<int:pk>/reply/', add_reply, name='add_reply'), 
    
]
