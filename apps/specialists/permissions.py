from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSpecialistOrReadOnly(BasePermission):
    """Permission class for objects associated with Specialist."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        pk = (view.kwargs.get('specialist_id')
              if view.kwargs.get('specialist_id') else view.kwargs.get('pk'))
        pk = pk.replace('-', '')
        return request.user.is_authenticated and str(request.user.pk.hex) == pk
