from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models.account import Account


class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
