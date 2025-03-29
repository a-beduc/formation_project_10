from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from myauth.models import User


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    """
    Custom admin configuration for the User model.
    """
    list_display = ('id', 'username', 'date_of_birth', 'can_be_contacted',
                    'can_data_be_shared', 'is_staff', 'is_superuser')
    search_fields = ('id', 'username')
    ordering = ('id',)
    list_filter = ('can_be_contacted', 'can_data_be_shared')
    fieldsets = (DefaultUserAdmin.fieldsets +
                 (("Softdesk API", {"fields": (
                     "date_of_birth",
                     "can_be_contacted",
                     "can_data_be_shared",
                 )}),))
