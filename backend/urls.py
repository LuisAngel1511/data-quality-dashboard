from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.http import JsonResponse

def root_view(request):
    # Página del dashboard (plantilla)
    return render(request, "dashboard.html")

def ping_view(request):
    return JsonResponse({"pong": True})

urlpatterns = [
    path("", root_view),                     # raíz (dashboard)
    path("ping/", ping_view),                # prueba rápida JSON
    path("admin/", admin.site.urls),
    path("api/", include("datasets.urls")),  # 👈 incluye las rutas de la API
]
