from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'phone_number', 'date_of_birth', 'address', 'gender', 'specialization', 'password1', 'password2'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if obj:  # Editing an existing user
            if obj.role == 'doctor':
                # Include specialization in fieldsets for doctors
                return super().get_fieldsets(request, obj)
            else:
                # Exclude specialization for non-doctors
                return [
                    (None, {'fields': ('username', 'password')}),
                    ('Personal info', {'fields': ('name', 'email', 'phone_number', 'address', 'date_of_birth', 'gender')}),
                    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
                ]
        else:  # Adding a new user
            # Always show specialization on creation if role is selected as doctor
            return [
                (None, {'classes': ('wide',), 'fields': ('username', 'email', 'name', 'phone_number', 'date_of_birth', 'address', 'gender', 'role', 'specialization', 'password1', 'password2')}),
            ]

    search_fields = ('username', 'email', 'name')
    list_filter = ('role', 'specialization')

    def get_list_display(self, request):
        # Customize list display based on user role or admin preferences
        return ('username', 'name', 'email', 'role')

admin.site.register(User, UserAdmin)
