from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

'''
role_based_redirect view is used to redirect the user based on the role of the user
- user: user object
- if user is staff, redirect to admin dashboard
- if user is doctor, redirect to doctor dashboard
- else redirect to default dashboard
'''
@login_required
def role_based_redirect(request):
    user = request.user
    if user.is_staff:
        return redirect('admin_dashboard')  # Redirect to custom admin dashboard
    elif user.is_doctor:
        return redirect('doctor_dashboard')  # Redirect to custom doctor dashboard
    else:
        return redirect('default_dashboard')  # Redirect to a general dashboard or homepage

'''
login_view view is used to display the login form
- if the form is valid, redirect to the respective dashboard
'''
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return role_based_redirect(request)
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})