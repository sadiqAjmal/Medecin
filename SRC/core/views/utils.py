from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

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
