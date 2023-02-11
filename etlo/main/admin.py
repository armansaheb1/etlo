from django.contrib import admin
from .models import CustomUser, MobileConfirmationCode, Notification, EmailConfirmationCode, Country, DepartmentService, DepartmentBanner, State, City, Department, Wallet, Currency, BankIcon, DepositSettings, Transaction, TransactionType, NotificationType


class DateAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
# Register your models here.


admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Currency)
admin.site.register(CustomUser)
admin.site.register(MobileConfirmationCode, DateAdmin)
admin.site.register(EmailConfirmationCode, DateAdmin)
admin.site.register(Notification, DateAdmin)
admin.site.register(Department)
admin.site.register(DepartmentBanner)
admin.site.register(DepartmentService)
admin.site.register(Wallet)
admin.site.register(BankIcon)
admin.site.register(DepositSettings)
admin.site.register(Transaction)
admin.site.register(TransactionType)
admin.site.register(NotificationType)
