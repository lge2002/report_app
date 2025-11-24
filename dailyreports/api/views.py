from datetime import date as _date, timedelta
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import connections
from django.views.decorators.http import require_GET

TABLE_MAP = {
    "srldc": "srldc_app_srldc2cdata",
    "processor": "srldc_app_srldc2adata",
}

STATE_ABBREV = {
    "andhra pradesh": "AP",
    "andhra": "AP",
    "karnataka": "KAR",
    "kerala": "KER",
    "pondicherry": "PONDY",
    "tamil nadu": "TN",
    "tamilnadu": "TN",
    "telangana": "TG",
    "region": "Region",
}

def rows_to_dicts(cursor):
    cols = [c[0] for c in cursor.description] if cursor.description else []
    return [dict(zip(cols, row)) for row in cursor.fetchall()]

@require_GET
def get_reports(request):
    date_str = request.GET.get("date")
    state = request.GET.get("state")
    tables_q = request.GET.get("tables", "srldc,processor")
    try:
        limit = int(request.GET.get("limit", 200))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("limit must be an integer")
    try:
        offset = int(request.GET.get("offset", 0))
    except (TypeError, ValueError):
        return HttpResponseBadRequest("offset must be an integer")

    # <-- DEFAULT TO YESTERDAY WHEN NO DATE PROVIDED -->
    if not date_str:
        yesterday = _date.today() - timedelta(days=1)
        date_str = yesterday.isoformat()

    if date_str:
        try:
            _date.fromisoformat(date_str)
        except ValueError:
            return HttpResponseBadRequest("date must be in YYYY-MM-DD format")

    keys = [k.strip() for k in tables_q.split(",") if k.strip()]
    if not keys:
        return HttpResponseBadRequest("at least one table key must be provided in 'tables'")

    tables = []
    for k in keys:
        if k in TABLE_MAP:
            tables.append((k, TABLE_MAP[k]))
        else:
            return HttpResponseBadRequest(f"unknown table key: {k}. Allowed keys: {', '.join(TABLE_MAP.keys())}")

    state_norm = (state or "").strip().lower()
    state_no_space = state_norm.replace(" ", "") if state_norm else ""
    state_abbrev = STATE_ABBREV.get(state_norm) if state_norm else None
    contains_pattern = f"%{state}%".replace(" ", "%") if state else None

    result = {}
    try:
        for key, table_name in tables:
            where = []
            params = []

            if date_str:
                where.append("report_date::date = %s")
                params.append(date_str)

            if state:
                state_fragments = []
                state_fragments.append("REPLACE(LOWER(state), ' ', '') = %s")
                params.append(state_no_space)
                state_fragments.append("LOWER(state) = %s")
                params.append(state_norm)
                if state_abbrev:
                    state_fragments.append("state = %s")
                    params.append(state_abbrev)
                state_fragments.append("state ILIKE %s")
                params.append(contains_pattern)

                where.append("(" + " OR ".join(state_fragments) + ")")

            where_sql = ("WHERE " + " AND ".join(where)) if where else ""
            sql = f"""
                SELECT *
                FROM {table_name}
                {where_sql}
                ORDER BY report_date DESC
                LIMIT %s OFFSET %s
            """

            with connections['default'].cursor() as cursor:
                cursor.execute(sql, params + [limit, offset])
                result[key] = rows_to_dicts(cursor)

    except Exception as e:
        return JsonResponse({'error': 'pg query failed', 'detail': str(e)}, status=500)

    return JsonResponse(result)
