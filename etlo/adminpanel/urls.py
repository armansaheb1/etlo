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
from django.urls import path
from . import views


urlpatterns = [
    path('login', views.Login.as_view()),
    path('set_admin', views.SetAdmin.as_view()),
    path('active_chats', views.ActiveChats.as_view()),
    path('user_chats', views.UserChats.as_view()),
    path('user_chats/<id>', views.UserChats.as_view()),
    path('currencies', views.Currencies.as_view()),
    path('currencies/<id>', views.Currencies.as_view()),
    path('wallets', views.Wallets.as_view()),
    path('wallets/<id>', views.Wallets.as_view()),
    path('chargewallets', views.ChargeWallets.as_view()),
    path('banners', views.Banners.as_view()),
    path('health_insurance_companies', views.HealthInsuranceCompanies.as_view()),
    path('health_insurance_price_lists',
         views.HealthInsurancePriceLists.as_view()),
    path('health_insurance_price_lists/<id>',
         views.HealthInsurancePriceLists.as_view()),
    path('health_insurance_companies/<id>',
         views.HealthInsuranceCompanies.as_view()),
    path('health_insurance_discounts', views.HealthInsuranceDiscounts.as_view()),
    path('health_insurance_discounts/<id>',
         views.HealthInsuranceDiscounts.as_view()),
    path('health_insurance_user_discounts',
         views.HealthInsuranceUserDiscounts.as_view()),
    path('health_insurance_user_discounts/<id>',
         views.HealthInsuranceUserDiscounts.as_view()),
    path('health_insurance_pendings', views.HealthInsurancePendings.as_view()),
    path('health_insurance_rejecteds', views.HealthInsuranceRejecteds.as_view()),
    path('health_insurance_submiteds', views.HealthInsuranceSubmiteds.as_view()),
    path('health_insurance_reject', views.HealthInsuranceReject.as_view()),
    path('health_insurance_submit', views.HealthInsuranceSubmit.as_view()),
    path('foreign_buy_pendings', views.ForeignBuyPendings.as_view()),
    path('foreign_buy_check_pendings', views.ForeignBuyCheckPendings.as_view()),
    path('foreign_buy_rejecteds', views.ForeignBuyRejecteds.as_view()),
    path('foreign_buy_submiteds', views.ForeignBuySubmiteds.as_view()),
    path('foreign_buy_reject', views.ForeignBuyReject.as_view()),
    path('foreign_buy_submit', views.ForeignBuySubmit.as_view()),
    path('departments', views.Departments.as_view()),
    path('departments/<id>', views.Departments.as_view()),
    path('department_banners', views.DepartmentBanners.as_view()),
    path('department_banners/<id>', views.DepartmentBanners.as_view()),
    path('department_services', views.DepartmentServices.as_view()),
    path('department_services/<id>', views.DepartmentServices.as_view()),
    path('active_countries', views.ActiveCountries.as_view()),
    path('active_countries/<id>', views.ActiveCountries.as_view()),
    path('foreign_buy_categories', views.ForeignBuyCategories.as_view()),
    path('foreign_buy_categories/<id>', views.ForeignBuyCategories.as_view()),
    path('foreign_buy_sites', views.ForeignBuySites.as_view()),
    path('foreign_buy_sites/<id>', views.ForeignBuySites.as_view()),
    path('bank_sheba_requests', views.BankShebaRequests.as_view()),
    path('bank_sheba_requests/<id>', views.BankShebaRequests.as_view()),
    path('bank_card_requests', views.BankCardRequests.as_view()),
    path('bank_card_requests/<id>', views.BankCardRequests.as_view()),
    path('id_requests', views.IdRequests.as_view()),
    path('id_request_rejecteds', views.IdRequestRejecteds.as_view()),
    path('id_requests/<id>', views.IdRequests.as_view()),
    path('image_requests', views.ImageRequests.as_view()),
    path('image_request_rejecteds', views.ImageRequestRejecteds.as_view()),
    path('image_requests/<id>', views.ImageRequests.as_view()),
    path('withdraw_requests/<id>', views.WithdrawRequests.as_view()),
    path('deposit_settings', views.DepositSetting.as_view()),
    path('transaction_type', views.TransactionTypes.as_view()),
    path('transaction_type/<id>', views.TransactionTypes.as_view()),

]
