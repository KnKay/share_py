from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated

class ReadOnly(BasePermission):
  def has_permission(self, request, view):
    return request.method in SAFE_METHODS


class LocationPermision(BasePermission):
  '''
  We need users to allow create
  '''

  def has_permission(self, request, view):
    return (request.method in SAFE_METHODS  or request.user.is_authenticated)

  def has_object_permission(self, request, view, obj):
      '''
      Objects should not be updated by users
      '''
      return (request.method in SAFE_METHODS or request.user.is_staff)
