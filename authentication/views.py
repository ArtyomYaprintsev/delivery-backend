from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import UserSerializer


class Login(ObtainAuthToken):
    pass


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserMe(APIView):
    serializer_class = UserSerializer

    def get(self, request, **kwargs):
        return Response(self.serializer_class(request.user).data)
