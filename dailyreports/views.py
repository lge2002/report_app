from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def psp(request):
    selected_state = request.session.get("selected_state")

    # ⭐ Capture the date from GET
    selected_date = request.GET.get("date")

    context = {
        'user': request.user,
        'title': 'PSP',
        'selected_state': selected_state,
        'selected_date': selected_date,     # ⭐ send date to template
    }
    return render(request, 'dailyreports/psp.html', context)



@login_required
def error_report(request):
    """
    View for the Data Tables page.
    """
    selected_state = request.session.get("selected_state")   # ⭐ added

    context = {
        'user': request.user,
        'title': 'Error Reports',
        'selected_state': selected_state                     # ⭐ added
    }
    return render(request, 'dailyreports/error_report.html', context)


@login_required
def monthly_error_report(request):
    """
    View for the Responsive Tables page.
    """
    selected_state = request.session.get("selected_state")   # ⭐ added

    context = {
        'user': request.user,
        'title': 'Monthly Error Reports',
        'selected_state': selected_state                     # ⭐ added
    }
    return render(request, 'dailyreports/monthly_error_report.html', context)


# --- Add these new views --- #
@login_required
def daily_comparison(request):
    """
    Renders the Daily Comparison - Chart page.
    Accessible via {% url 'daily_comparison' %}
    """
    selected_state = request.session.get("selected_state")
    # optional GET params you might use for chart filters
    date = request.GET.get("date")
    month = request.GET.get("month")
    year = request.GET.get("year")

    context = {
        "user": request.user,
        "title": "Daily Comparison - Chart",
        "selected_state": selected_state,
        "date": date,
        "month": month,
        "year": year,
        # preview image (your uploaded file path)
        "preview_image": "/mnt/data/979ee8e8-59f4-47a7-add1-68f484a32caf.png",
    }
    return render(request, "dailyreports/daily_comparison.html", context)


@login_required
def daily_windy_power(request):
    """
    Renders the Daily Wind Report Generation page.
    Accessible via {% url 'daily_windy_power' %}
    """
    selected_state = request.session.get("selected_state")
    # optional GET params for the report generation
    date = request.GET.get("date")
    params = {
        "user": request.user,
        "title": "Daily Wind Report Generation",
        "selected_state": selected_state,
        "date": date,
        "preview_image": "/mnt/data/979ee8e8-59f4-47a7-add1-68f484a32caf.png",
    }
    return render(request, "dailyreports/daily_windy_power.html", params)


@login_required
def run_daily_dsm(request):
    """
    Renders a page to trigger/run the Daily DSM process.
    Accessible via {% url 'run_daily_dsm' %}
    If this view should actually trigger a backend job, add that logic here.
    """
    selected_state = request.session.get("selected_state")
    # Example: read optional job parameters from GET
    run_for_date = request.GET.get("run_date")

    context = {
        "user": request.user,
        "title": "RUN Daily DSM",
        "selected_state": selected_state,
        "run_for_date": run_for_date,
        "preview_image": "/mnt/data/979ee8e8-59f4-47a7-add1-68f484a32caf.png",
    }
    return render(request, "dailyreports/run_daily_dsm.html", context)


@login_required
def accuracy_report(request):
    """
    Renders the Accuracy Report & Remarks page.
    Accessible via {% url 'Accuracy_report' %}
    Note: view name matches your template/URL name you provided.
    """
    selected_state = request.session.get("selected_state")
    # optional filters
    month = request.GET.get("month")
    year = request.GET.get("year")

    context = {
        "user": request.user,
        "title": "Accuracy Report & Remarks",
        "selected_state": selected_state,
        "month": month,
        "year": year,
        "preview_image": "/mnt/data/979ee8e8-59f4-47a7-add1-68f484a32caf.png",
    }
    return render(request, "dailyreports/accuracy_report.html", context)
