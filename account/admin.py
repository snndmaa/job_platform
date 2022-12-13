from django.contrib import admin
from account.models import Account, UserProfile, Credit

# Register your models here.
admin.site.register(Account)
admin.site.register(UserProfile)
admin.site.register(Credit)