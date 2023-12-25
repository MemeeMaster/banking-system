from django.contrib import admin

from .models import Account, BankUser

# Register your models here.

admin.site.register(BankUser)
admin.site.register(Account)