from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# Define the homepage view
def home_view(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/climate/', include('climate.urls')),  # Climate app URLs
    path('', home_view, name='home'),  # Root URL
]
