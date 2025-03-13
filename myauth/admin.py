from atexit import register

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from myauth.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'date_of_birth', 'can_be_contacted', 'can_data_be_shared')
    search_fields = ('id', 'username')
    ordering = ('id',)
    list_filter = ('can_be_contacted', 'can_data_be_shared')
