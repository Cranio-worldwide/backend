from rest_framework import viewsets

from .models import DoctorUser
from .serializers import DoctorUserSerializer


class DoctorUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели DoctorUser."""

    queryset = DoctorUser.objects.all()
    serializer_class = DoctorUserSerializer
