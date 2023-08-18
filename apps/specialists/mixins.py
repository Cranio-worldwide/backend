from django.shortcuts import get_object_or_404

from .models import Specialist
from .permissions import IsSpecialistOrReadOnly


class SpecBasedMixin:
    """Abstract class for Spec attributes: Addresses, Documents."""
    permission_classes = (IsSpecialistOrReadOnly,)

    def get_specialist(self):
        return get_object_or_404(Specialist,
                                 pk=self.kwargs.get('specialist_id'))

    def perform_create(self, serializer):
        serializer.save(specialist=self.request.user)
