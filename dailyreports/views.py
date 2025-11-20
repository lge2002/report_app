from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def psp(request):
    """
    View for the Basic Tables page.
    """
    context = {
        'user': request.user,
        'title': 'Basic Tables'
    }
    return render(request, 'dailyreports/psp.html', context)


@login_required
def error_report(request):
    """
    View for the Data Tables page.
    """
    context = {
        'user': request.user,
        'title': 'Data Tables'
    }
    return render(request, 'dailyreports/error_report.html', context)


@login_required
def monthly_error_report(request):
    """
    View for the Responsive Tables page.
    """
    context = {
        'user': request.user,
        'title': 'Responsive Tables'
    }
    return render(request, 'dailyreports/monthly_error_report.html', context)
