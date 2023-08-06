from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Specialist


class IsSpecialistOrReadOnly(BasePermission):
    """Permission class for objects associated with Specialist."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        pk = (view.kwargs.get('specialist_id')
              if view.kwargs.get('specialist_id') else view.kwargs.get('pk'))
        return get_object_or_404(Specialist, pk=pk) == request.user
