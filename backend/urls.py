from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import JsonResponse

def root_view(request):
    return render(request, "dashboard.html")

def api_health(_):
    return JsonResponse({"ok": True, "where": "backend.urls"})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", api_health),          # ← PRUEBA A
    path("api/", include("datasets.urls")),   # ← API de la app
    path("", root_view),
]
