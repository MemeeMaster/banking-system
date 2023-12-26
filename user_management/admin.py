from django.contrib import admin

from .models import Account, BankUser, Currency


# Register your models here.

class BankUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    list_filter = ("first_name", "last_name", "email")
    ordering = ("first_name", "last_name", "email")


class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_number", "currency", "owner")
    list_filter = ("owner",)
    ordering = ("owner", "currency")


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "exchange_rate")
    list_filter = ("code", "name", "exchange_rate")
    ordering = ("code", "name", "exchange_rate")


admin.site.register(BankUser, BankUserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Currency, CurrencyAdmin)
