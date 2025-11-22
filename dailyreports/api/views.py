from django.http import JsonResponse, HttpResponseBadRequest
from django.db import connections
from django.views.decorators.http import require_GET

def rows_to_dicts(cursor):
    cols = [c[0] for c in cursor.description]
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

@require_GET
def get_reports(request):
    date = request.GET.get("date")
    state = request.GET.get("state")
    try:
        limit = int(request.GET.get("limit", 200))
    except ValueError:
        return HttpResponseBadRequest("limit must be integer")

    where = []
    params = []
    if date:
        where.append("report_date = %s")
        params.append(date)
    if state:
        where.append("a_z_state = %s")
        params.append(state)
    where_sql = ("WHERE " + " AND ".join(where)) if where else ""

    srldc_sql = f"SELECT * FROM srldc_app_srldc2cdata {where_sql} ORDER BY report_date DESC LIMIT %s"
    processor_sql = f"SELECT * FROM srldc_app_srldc2cdata {where_sql} ORDER BY report_date DESC LIMIT %s"

    result = {"srldc": [], "processor": []}

    try:
        with connections['default'].cursor() as cursor:
            cursor.execute(srldc_sql, params + [limit])
            result['srldc'] = rows_to_dicts(cursor)

        with connections['default'].cursor() as cursor:
            cursor.execute(processor_sql, params + [limit])
            result['processor'] = rows_to_dicts(cursor)
    except Exception as e:
        # return a useful JSON error instead of full traceback
        return JsonResponse({'error': 'pg query failed', 'detail': str(e)}, status=500)

    return JsonResponse(result)
