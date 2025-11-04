from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.shortcuts import get_object_or_404

from .models import Dataset
from .serializers import DatasetSerializer
from .services.ingestion import load_and_profile
from .services.profiling import nulls_per_column, duplicates_info, distribution

class DatasetList(generics.ListAPIView):
    """Lista datasets con esquema y KPIs básicos (perfil en caché)."""
    queryset = Dataset.objects.all().order_by("-created_at")
    serializer_class = DatasetSerializer

class DatasetUpload(APIView):
    """Sube un CSV/Parquet y genera el perfil inicial."""
    def post(self, request):
        file = request.FILES.get("file")
        name = request.data.get("name") or (file and file.name)
        if not file:
            return Response({"error": "archivo requerido (file)"}, status=status.HTTP_400_BAD_REQUEST)
        ds = Dataset.objects.create(name=name, file=file)
        load_and_profile(ds)
        return Response({"dataset_id": ds.id}, status=status.HTTP_201_CREATED)

class DatasetSchema(APIView):
    """Devuelve info del dataset: columnas, roles y KPIs del perfil."""
    def get(self, _, pk):
        ds = get_object_or_404(Dataset, pk=pk)
        return Response(DatasetSerializer(ds).data)

class DatasetNulls(APIView):
    """Nulos totales y por columna."""
    def get(self, _, pk):
        ds = get_object_or_404(Dataset, pk=pk)
        return Response(nulls_per_column(ds.file.path))

class DatasetDuplicates(APIView):
    """Conteo de duplicados y muestra de filas duplicadas."""
    def get(self, _, pk):
        ds = get_object_or_404(Dataset, pk=pk)
        return Response(duplicates_info(ds.file.path))

class DatasetDistribution(APIView):
    """Distribución de una columna (histograma numérico o conteos categóricos)."""
    def get(self, request, pk):
        col = request.query_params.get("col")
        bins = int(request.query_params.get("bins", 20))
        if not col:
            return Response({"error": "param 'col' requerido"}, status=status.HTTP_400_BAD_REQUEST)
        ds = get_object_or_404(Dataset, pk=pk)
        return Response(distribution(ds.file.path, col, bins))
