import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.core.exceptions import ValidationError
# from .serializers import UserSignupSerializer,LoginSerializer,UserProfileUpdateSerializer
logger = logging.getLogger(__name__)


class UserUploadBook(APIView):
    def post (self,request):
        pass