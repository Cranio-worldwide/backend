from djoser.views import UserViewSet as DjoserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.core.services.ip_location import (
    get_geodata, get_user_ip_address, parse_coordinates,
)


class UserViewSet(DjoserViewSet):
    """Customized version of Djoser UserViewSet."""
    @action(["get"], detail=False, permission_classes=(AllowAny,))
    def me_where(self, request):
        """Returns coordinates of user basing on IP address."""
        ip_address = get_user_ip_address(request)
        geodata = get_geodata(ip_address)
        coordinates = parse_coordinates(geodata)
        data = {"coordinates": coordinates}
        return Response(data)


# class VerifyEmail(APIView):
#     """Temporary solution to make registration work without frontend"""
#     def get(self, request, uid, token):
#         protocol = 'https://' if request.is_secure() else 'http://'
#         web_url = protocol + request.get_host()
#         post_url = web_url + "/api/v1/users/activation/"
#         payload = {'uid': uid, 'token': token}
#         result = requests.post(post_url, data=payload)
#         if result.status_code == status.HTTP_204_NO_CONTENT:
#             return HttpResponse(content='Account was succesfully activated')
#         content = result.text
#         return HttpResponse(content)


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
