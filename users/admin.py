from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User

# # This should be done in a migration or a signal, not in the admin class
# # Ensure that this group is created only if it doesn't already exist
# if not Group.objects.filter(name='Doctor').exists():
#     Group.objects.create(name='Doctor')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (None, {
            'fields': ('username',
            'email', 'password1', 'password2', 'is_doctor', 'is_patient')
        }),
    )
    
    fieldsets = (
        (None, {
            'fields': ('username',
            'email', 'password', 'is_doctor', 'is_patient')
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
