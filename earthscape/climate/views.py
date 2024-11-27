from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import ClimateDataset
from .serializers import ClimateDatasetSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
import matplotlib.pyplot as plt
import io
import urllib, base64

class DataUploadView(APIView):
    # Specify the parser classes for handling file uploads and form data
    parser_classes = [MultiPartParser, FormParser]
    
    # Add authentication and permission classes
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]  # Only authenticated users can upload

    def post(self, request, *args, **kwargs):
        # Initialize the serializer with the incoming request data (dataset details)
        serializer = ClimateDatasetSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the dataset and associate it with the current user (request.user)
            serializer.save(uploaded_by=request.user)
            return Response({"message": "Dataset uploaded successfully!"}, status=201)
        
        # Return error response if serializer is invalid
        return Response(serializer.errors, status=400)


class ClimateDatasetListView(APIView):
    """
    API endpoint to list all climate datasets.
    Admins or analysts can view the datasets.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve all datasets
        datasets = ClimateDataset.objects.all()
        # Serialize the dataset data
        serializer = ClimateDatasetSerializer(datasets, many=True)
        return Response(serializer.data)


class ClimateDatasetDetailView(APIView):
    """
    API endpoint to retrieve, update or delete a specific climate dataset.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ClimateDataset.objects.get(pk=pk)
        except ClimateDataset.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        dataset = self.get_object(pk)
        if dataset is None:
            return Response({"error": "Dataset not found"}, status=404)
        
        serializer = ClimateDatasetSerializer(dataset)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        dataset = self.get_object(pk)
        if dataset is None:
            return Response({"error": "Dataset not found"}, status=404)
        
        serializer = ClimateDatasetSerializer(dataset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Dataset updated successfully!"})
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, *args, **kwargs):
        dataset = self.get_object(pk)
        if dataset is None:
            return Response({"error": "Dataset not found"}, status=404)
        
        dataset.delete()
        return Response({"message": "Dataset deleted successfully!"}, status=204)
    


class ClimateDataVisualizationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve climate datasets
        datasets = ClimateDataset.objects.all()

        # Serialize the data
        serializer = ClimateDatasetSerializer(datasets, many=True)

        # Generate a simple plot using Matplotlib
        temperatures = [dataset['temperature'] for dataset in serializer.data]
        dates = [dataset['upload_date'] for dataset in serializer.data]

        # Create a plot
        plt.plot(dates, temperatures)
        plt.title('Temperature Trends')
        plt.xlabel('Date')
        plt.ylabel('Temperature')

        # Save plot to a BytesIO object
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()

        # Return the plot as an image embedded in base64 format
        return Response({"message": "Dataset visualization", "plot": image_data})
