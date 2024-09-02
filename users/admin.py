from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
# from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'is_doctor', 'is_patient'),
        }),
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'phone_number', 'password', 'is_doctor', 'is_patient'),
        }),
    )

    list_display = ('username', 'email', 'is_staff', 'is_doctor', 'is_patient')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers see all users
        return qs.filter(is_doctor=False)  # Restrict regular staff from seeing doctors

    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete users
        return request.user.is_superuser
