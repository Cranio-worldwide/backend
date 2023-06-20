import requests

from django.http import HttpResponse
from djoser.views import UserViewSet as DjoserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
# from djoser import signals
# from djoser.conf import settings

from apps.core.services.ip_location import (
    get_geodata, get_user_ip_address, parse_coordinates,
)
from apps.specialists.serializers import MeSpecialistSerializer
from apps.users.models import CustomUser

from .serializers import UserSerializer


class UserViewSet(DjoserViewSet):

    @action(["get", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            if request.user.role == CustomUser.Role.SPECIALIST:
                serializer = MeSpecialistSerializer(request.user)
            if request.user.role == CustomUser.Role.ADMIN:
                serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    @action(["get"], detail=False)
    def me_where(self, request):
        ip_address = get_user_ip_address(request)
        geodata = get_geodata(ip_address)
        coordinates = parse_coordinates(geodata)
        data = {"coordinates": coordinates}
        return Response(data)

    # def perform_create(self, serializer, *args, **kwargs):
    #     super().perform_create(serializer, *args, **kwargs)
    #     user = serializer.instance
    #     user.is_active = True
    #     user.save()


    # @action(["post"], detail=False)
    # def activation(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.user
    #     user.is_verified = True
    #     user.save()

    #     signals.user_activated.send(
    #         sender=self.__class__, user=user, request=self.request
    #     )

    #     context = {"user": user}
    #     to = [user.email]
    #     settings.EMAIL.confirmation(self.request, context).send(to)

    #     return Response(status=status.HTTP_204_NO_CONTENT)


class VerifyEmail(APIView):
    """Temporary solution to make registration work without frontend"""
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/api/v1/auth/users/activation/"
        payload = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=payload)
        if result.status_code == status.HTTP_204_NO_CONTENT:
            return HttpResponse(content='Account was succesfully activated')
        content = result.text
        return HttpResponse(content)


# КОД НАСТИ НА РЕГИСТРАЦИЮ И АКТИВАЦИЯ ПОЧТЫ, ОСТАВЛЯЮ ПОКА ТУТ
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
