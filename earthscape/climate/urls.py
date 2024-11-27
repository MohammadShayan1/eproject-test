# urls.py
from django.urls import path
from .views import DataUploadView, ClimateDatasetListView, ClimateDatasetDetailView

urlpatterns = [
    path('upload/', DataUploadView.as_view(), name='data-upload'),
    path('datasets/', ClimateDatasetListView.as_view(), name='dataset-list'),
    path('datasets/<int:pk>/', ClimateDatasetDetailView.as_view(), name='dataset-detail'),
]
