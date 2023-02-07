from django.contrib import admin

from .models import ForeignBuyRequests, ForeignBuyPost
# Register your models here.
admin.site.register(ForeignBuyRequests)
admin.site.register(ForeignBuyPost)
