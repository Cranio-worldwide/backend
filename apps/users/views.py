import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language_from_request
from django_filters.rest_framework import DjangoFilterBackend
from djoser import signals
from djoser.views import UserViewSet as DjoserUserViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import LimitOffsetPagination

from .models import CustomUser
from .utils import send_verification_email


class UserViewSet(DjoserUserViewSet):
    queryset = CustomUser.objects.all()

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        # context = {"user": user}
        language = get_language_from_request(self.request, check_path=True)
        send_verification_email(self.request, user, language)
        

# class RegisterView(APIView):
#     """Viewset for users' registaration with JWT."""

#     serializer_class = SpecialistCreateSerializer

#     def post(self, request):
#         language = get_language_from_request(request, check_path=True)
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         user = get_object_or_404(
#             Specialist,
#             email=serializer.data['email'])

#         send_verification_email(request, user, language)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class VerifyEmail(APIView):
#     """Viewset for email verification with JWT."""

#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             data = jwt.decode(token, settings.SECRET_KEY)
#             user = get_object_or_404(Specialist, id=data['user_id'])
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#                 data = {
#                     'email': settings.CONSTANTS['EMAIL_SUCCESS_MESSEGE']
#                 }

#                 return Response(data, status=status.HTTP_200_OK)

#         except jwt.ExpiredSignatureError:
#             data = {
#                 'error': settings.CONSTANTS['TOKEN_EXPIRED']
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError:
#             data = {
#                 'error': settings.CONSTANTS['TOKEN_INVALID']
#             }
#             return Response(data, status=status.HTTP_400_BAD_REQUEST)
