
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.settings import api_settings
from .models import Category, Location
from .serializers import CategorySerializer, LocationSerializer, ItemSerializer
from .permissions import ReadOnly, LocationPermision

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly | IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly | IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = ItemSerializer

# As we want to have at least work as needed and locations should be an easy thing:
# Create = get or create (as we will have persons sharhing the location)
class LocationViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly | LocationPermision]
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            instance, created = serializer.get_or_create()
            if not created:
                serializer.update(instance, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
