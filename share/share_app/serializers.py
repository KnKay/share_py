import copy

from rest_framework import serializers
import rest_framework.validators
from .models import Category, Location, Item

class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item
    fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
  class Meta:
      model = Location
      fields = '__all__'
  # https://techstream.org/bits/get_or_create-in-django-rest-framework/
  def run_validators(self, value):
    for validator in copy.copy(self.validators):
      if isinstance(validator,  rest_framework.validators.UniqueTogetherValidator):
        self.validators.remove(validator)
    super(LocationSerializer, self).run_validators(value)

  def get_or_create(self):
    defaults = self.validated_data.copy()
    return Location.objects.get_or_create(
       city=self.validated_data["city"],
       post_code=self.validated_data["post_code"],
       defaults=defaults)


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data["access_token"] = data["access"]
        data["refresh_token"] = data["refresh"]
        return data
