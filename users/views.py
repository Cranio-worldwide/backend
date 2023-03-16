from rest_framework import viewsets

from .models import DoctorUser
from .serializers import DoctorUserSerializer


class DoctorUserViewSet(viewsets.ModelViewSet):
    """DoctorUser model view set."""

    queryset = DoctorUser.objects.all()
    serializer_class = DoctorUserSerializer
