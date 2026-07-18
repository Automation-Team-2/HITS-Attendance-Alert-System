"""Dashboard views — page rendering only.
Data API is served by FastAPI on port 8001.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def login_view(request):
    """Render login page. Redirect to dashboard if already authenticated."""
    if request.user.is_authenticated:
        return render(request, 'dashboard/index.html')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'dashboard/index.html')
        error = 'Invalid username or password.'
    return render(request, 'registration/login.html', {'error': error})


@login_required
def dashboard_view(request):
    """Main dashboard — only accessible to logged-in users."""
    return render(request, 'dashboard/index.html')


def logout_view(request):
    """Log out and redirect to login page."""
    logout(request)
    return render(request, 'registration/login.html', {'logged_out': True})
