from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_doctor')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers see all users
        return qs.filter(is_doctor=False)  # Restrict regular staff from seeing doctors

    def has_delete_permission(self, request, obj=None):
        # Only superusers can delete users
        return request.user.is_superuser
