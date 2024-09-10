from django.shortcuts import redirect, render
from django.views import View, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm

class RoleBasedRedirectView(LoginRequiredMixin, RedirectView):
    """
    View class for role-based redirection.
    Redirects the user to a specific dashboard based on their role.
    """
    def get_redirect_url(self, *args, **kwargs):
        """
        Returns the URL to redirect the user based on their role.
        """
        user = self.request.user
        if user.is_staff:
            return 'admin_dashboard'  # Redirect to custom admin dashboard
        elif user.is_doctor:
            return 'doctor_dashboard'  # Redirect to custom doctor dashboard
        else:
            return 'default_dashboard'  # Redirect to a general dashboard or homepage


class LoginView(View):
    """
    View class for handling user login.
    """
    def get(self, request):
        """
        Handles GET request for login page.
        If the user is already authenticated, redirects to role-based redirection view.
        """
        if request.user.is_authenticated:
            return redirect('role_based_redirect')
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        """
        Handles POST request for login page.
        If the form is valid, redirects to role-based redirection view.
        """
        form = LoginForm(request.POST)
        if form.is_valid():
            return redirect('role_based_redirect')
        return render(request, 'users/login.html', {'form': form})
