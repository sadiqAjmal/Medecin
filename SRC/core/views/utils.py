from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.cache import cache

class AdminRequiredMixin(UserPassesTestMixin):
    """
    A mixin for views that require the user to be an admin or superuser.
    """

    def test_func(self):
        """
        Check if the user is an admin or superuser.
        """
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        """
        Handle the case when the user does not have permission to access the page.
        """
        raise PermissionDenied("You must be an admin or superuser to access this page.")


class DoctorRequiredMixin(UserPassesTestMixin):
    """
    A mixin for views that require the user to be a doctor.
    """

    def test_func(self):
        """
        Check if the user is an authenticated doctor.
        """
        return (
            self.request.user.is_authenticated
            and hasattr(self.request.user, 'is_doctor')
            and self.request.user.is_doctor
        )

    def handle_no_permission(self):
        """
        Handle the case when the user does not have permission to access the page.
        """
        raise PermissionDenied("You must be a doctor to access this page.")


def is_admin(user):
    """
    Check if the user is an admin.

    Args:
        user: The user object.

    Returns:
        True if the user is an admin, False otherwise.
    """
    return user.is_authenticated and user.is_staff


def is_doctor(user):
    """
    Check if the user is a doctor.

    Args:
        user: The user object.

    Returns:
        True if the user is a doctor, False otherwise.
    """
    return (
        user.is_authenticated
        and hasattr(user, 'is_doctor')
        and user.is_doctor
    )


def invalidate_cache(doctor_id, appointment_id):
    """
    Invalidate cache entries related to a specific doctor and appointment.

    Args:
        doctor_id: The ID of the doctor.
        appointment_id: The ID of the appointment.
    """
    # Delete all cache entries related to the specific doctor
    cache_key_pattern_doctor = f"appointments_page_*_{doctor_id}_doctor"
    cache.delete_pattern(cache_key_pattern_doctor)

    # Delete all cache entries starting with 'appointments' and ending with 'admin'
    cache_key_pattern_admin = "appointments*admin"
    cache.delete_pattern(cache_key_pattern_admin)

    cache.delete(f'appointment_{appointment_id}')