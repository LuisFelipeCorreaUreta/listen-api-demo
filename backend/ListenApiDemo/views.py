from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
import os
import requests

MASHAPE_KEY = os.environ.get("MASHAPE_KEY", "")

@require_http_methods(["GET"])
def search(request):
    query = request.GET.get("q")
    sort_by_date = request.GET.get("sort_by_date")
    result_type = request.GET.get("type")

    head_response = requests.head("https://listennotes.p.mashape.com/api/v1/search",
            headers={
                "X-Mashape-Key": MASHAPE_KEY,
                "Accept": "application/json"
                }
            )
    if 'X-Ratelimit-full-text-search-quota-Remaining' in head_response.headers and head_response.headers['X-Ratelimit-full-text-search-quota-Remaining'] == 0:
        return HttpResponse(status=429)

    response = requests.get("https://listennotes.p.mashape.com/api/v1/search?q={}&sort_by_date={}&type={}".format(query, sort_by_date, result_type),
            headers={
                "X-Mashape-Key": MASHAPE_KEY,
                "Accept": "application/json"
                }
            )
    return JsonResponse(response.json())