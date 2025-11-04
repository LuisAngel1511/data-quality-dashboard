from django.urls import path
from .views import (
    DatasetList, DatasetUpload, DatasetSchema,
    DatasetNulls, DatasetDuplicates, DatasetDistribution
)

urlpatterns = [
    path("datasets/", DatasetList.as_view()),
    path("datasets/upload/", DatasetUpload.as_view()),
    path("datasets/<int:pk>/schema/", DatasetSchema.as_view()),
    path("datasets/<int:pk>/nulls/", DatasetNulls.as_view()),
    path("datasets/<int:pk>/duplicates/", DatasetDuplicates.as_view()),
    path("datasets/<int:pk>/distributions/", DatasetDistribution.as_view()),
]
