"""Etlo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class_based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('health_insurance_details', views.HealthInsuranceDetails.as_view()),
    path('health_insurance_price_list',
         views.HealthInsurancePriceLists.as_view()),
    path('health_insurance_price_list2',
         views.HealthInsurancePriceLists2.as_view()),
    path('health_insurance_request', views.HealthInsuranceRequests.as_view()),
    path('my_insurances', views.MyInsurances.as_view()),
    path('check_discount', views.CheckDiscount.as_view()),
]
