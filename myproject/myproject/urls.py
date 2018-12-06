"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from myapp import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('loginform', views.loginform, name='home'),
    path('adminview',views.adminview,name='home'),
    path('trainerview',views.trainerview,name='home'),
    path('traineeview',views.traineeview,name='home'),
    path('addtrainee',views.addtrainee,name='home'),
    path('addtrainer',views.addtrainer,name='home'),
    path('feedback',views.feedback,name='home'),
    path('viewfeedback',views.viewfeedback,name='home'),
]