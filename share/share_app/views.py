
from django.http import HttpResponse
from rest_framework import serializers, viewsets
from rest_framework.permissions import IsAdminUser
from .models import Category
from .serializers import CategorySerializer
from .permissions import ReadOnly

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# ViewSets define the view behavior.
class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly | IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
