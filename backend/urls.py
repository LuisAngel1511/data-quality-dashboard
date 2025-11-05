from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import render

def root_view(request):
    # renderiza la plantilla del dashboard
    return render(request, "dashboard.html")

urlpatterns = [
    path("", root_view),                    #  página del dashboard
    path("admin/", admin.site.urls),
    path("api/", include("datasets.urls")), # API ya existente
]
