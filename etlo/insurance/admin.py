from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import HealthInsuranceCompany, HealthInsurancePriceList, HealthInsuranceRequest, HealthInsuranceUserDiscount


admin.site.register(HealthInsurancePriceList)
admin.site.register(HealthInsuranceCompany)
admin.site.register(HealthInsuranceRequest)
admin.site.register(HealthInsuranceUserDiscount)