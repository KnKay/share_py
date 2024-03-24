from django.db import models
import json

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length = 64)
  description = models.TextField()

  def __str__(self):
    return json.dumps(self)
