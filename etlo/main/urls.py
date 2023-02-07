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
    path('getimage', views.GetImage.as_view()),
    path('bankicons', views.BankIconsCard.as_view()),
    path('bankiconcards', views.BankIconsCard.as_view()),
    path('bankiconshebas', views.BankIconsSheba.as_view()),
    path('addresses', views.Addresses.as_view()),
    path('addresses/<id>', views.Addresses.as_view()),
    path('currencies', views.Currencies.as_view()),
    path('currency/<id>', views.CurrencyById.as_view()),
    path('withdraw', views.Withdraws.as_view()),
    path('withdraw/<id>', views.Withdraws.as_view()),
    path('balances', views.Balances.as_view()),
    path('transactions', views.Transactions.as_view()),
    path('activebankcards', views.ActiveBankCards.as_view()),
    path('activebankshebas', views.ActiveBankShebas.as_view()),
    path('chats_service/<department>/<service>', views.ChatsSer.as_view()),
    path('chats_department/<department>', views.ChatsDep.as_view()),
    path('chats', views.Chats.as_view()),
    path('chats_unreads_service/<department>/<service>',
         views.ChatsUnreadsSer.as_view()),
    path('chats_unreads_department/<department>',
         views.ChatsUnreadsDep.as_view()),
    path('chats_unreads', views.ChatsUnreads.as_view()),
    path('countries', views.Countries.as_view()),
    path('currency_convert', views.CurrencyConvert.as_view()),
    path('states/<id>', views.States.as_view()),
    path('cities/<id>', views.Cities.as_view()),
    path('active_countries', views.ActiveCountries.as_view()),
    path('banners', views.Banners.as_view()),
    path('departments', views.Departments.as_view()),
    path('departments/<id>/services', views.DepartmentsServices.as_view()),
    path('bankcards', views.BankCards.as_view()),
    path('bankcards/<id>', views.BankCards.as_view()),
    path('bankshebas', views.BankShebas.as_view()),
    path('bankshebas/<id>', views.BankShebas.as_view()),
    path('login', views.Login.as_view()),
    path('notification', views.Notifications.as_view()),
    path('current_user', views.CurrentUser.as_view()),
    path('check_phone', views.CheckPhone.as_view()),
    path('create_code', views.CreateCode.as_view()),
    path('create_email_code', views.CreateEmailCode.as_view()),
    path('set_profile_details', views.SetProfileDetails.as_view()),
    path('set_email', views.SetEmail.as_view()),
    path('set_phone', views.SetPhone.as_view()),
    path('set_password', views.SetPassword.as_view()),
]
