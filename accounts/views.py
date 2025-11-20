# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm  # keep your SignUpForm in accounts/forms.py
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

User = get_user_model()


def signup_view(request):
    """
    Simple signup view that uses your SignUpForm.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created. You can log in now.")
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """
    Login view: uses AuthenticationForm and safely handles `next`.
    """
    next_url = request.GET.get('next') or request.POST.get('next') or None
    if isinstance(next_url, str) and next_url.lower() == 'none':
        next_url = None

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        # style widgets if you like (view already did this earlier)
        try:
            form.fields['username'].widget.attrs.update({
                'class': 'py-2.5 px-4 block w-full border border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'example@example.com'
            })
            form.fields['password'].widget.attrs.update({
                'class': 'py-2.5 px-4 block w-full border border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Your Password'
            })
        except Exception:
            # if form structure differs, ignore styling step
            pass

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")

            # Only redirect to next_url when it looks safe.
            if next_url:
                allowed = url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host(), *getattr(settings, 'ALLOWED_HOSTS', [])},
                    require_https=request.is_secure(),
                )
                if allowed:
                    return redirect(next_url)

            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials. Try again.")
    else:
        form = AuthenticationForm()
        # try to set same widget classes for GET
        try:
            form.fields['username'].widget.attrs.update({
                'class': 'py-2.5 px-4 block w-full border border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'example@example.com'
            })
            form.fields['password'].widget.attrs.update({
                'class': 'py-2.5 px-4 block w-full border border-gray-200 rounded-lg sm:text-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'Your Password'
            })
        except Exception:
            pass

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


@require_POST
def logout_view(request):
    """
    Logout via POST and redirect to login.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    Dashboard view - keep simple and resilient.
    """
    context = {'user': request.user}
    return render(request, 'accounts/dashboard.html', context)

