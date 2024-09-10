from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.cache import cache

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("You must be an admin or superuser to access this page.")

class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and hasattr(self.request.user, 'is_doctor') and self.request.user.is_doctor

    def handle_no_permission(self):
        raise PermissionDenied("You must be a doctor to access this page.")



def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_doctor(user):
    return user.is_authenticated and hasattr(user, 'is_doctor') and user.is_doctor


def invalidate_cache(doctor_id,appointment_id):
    # Delete all cache entries related to the specific doctor
    cache_key_pattern_doctor = f"appointments_page_*_{doctor_id}_doctor"
    cache.delete_pattern(cache_key_pattern_doctor)

    # Delete all cache entries starting with 'appointments' and ending with 'admin'
    cache_key_pattern_admin = "appointments*admin"
    cache.delete_pattern(cache_key_pattern_admin)

    cache.delete(f'appointment_{appointment_id}')