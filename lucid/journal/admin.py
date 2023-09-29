from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm
from .models import JournalEntry, CustomUser


class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username"]







# Register your models here.
admin.site.register(JournalEntry)
admin.site.register(CustomUser, CustomUserAdmin)