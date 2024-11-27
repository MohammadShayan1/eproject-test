# serializers.py
from rest_framework import serializers
from .models import ClimateDataset

class ClimateDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimateDataset
        fields = ['id', 'name', 'file', 'uploaded_by', 'upload_date']
        read_only_fields = ['uploaded_by', 'upload_date']  # These fields are auto-filled
