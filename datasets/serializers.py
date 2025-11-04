from rest_framework import serializers
from .models import Dataset, Column, Profile

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ["name", "dtype_detected", "role"]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["stats_json"]

class DatasetSerializer(serializers.ModelSerializer):
    columns = ColumnSerializer(many=True, read_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Dataset
        fields = ["id", "name", "n_rows", "n_cols", "created_at", "columns", "profile"]
