import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.core.exceptions import ValidationError
from .serializers import UserSignupSerializer,LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
logger = logging.getLogger(__name__)

class UserSignupView(APIView):
    
    permission_classes = [AllowAny]  
    def post(self, request):
       
        try:
            serializer = UserSignupSerializer(data=request.data)
            
            if not serializer.is_valid():
                logger.warning(f"User signup validation failed: {serializer.errors}")
                return Response(
                    {
                        "status": "error",
                        "message": "Invalid input data",
                        "errors": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            
            logger.info("New user registered successfully")
            return Response(
                {
                    "status": "success",
                    "message": "User registered successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            logger.error(f"Validation error during user signup: {str(e)}")
            return Response(
                {
                    "status": "error",
                    "message": "Validation error",
                    "errors": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            logger.critical(f"Unexpected error in UserSignupView: {str(e)}", exc_info=True)
            return Response(
                {
                    "status": "error",
                    "message": "An unexpected error occurred",
                    
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    
   
class Login(APIView):
    permission_classes = [AllowAny]  
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            
            if not serializer.is_valid():
                return Response(
                    {
                        "status":"error",
                        "message":"User Login validation failed",
                        "errors": serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            email =serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                refresh_token= RefreshToken.for_user(user)
                access_token = refresh_token.access_token
                response= Response(
                    {
                        "status":'success',
                        "message":'Login Successful',
                        "access_token": str(access_token),
                        "refresh_token": str(refresh_token)
                    },
                    status= status.HTTP_200_OK
                )
                
                return response
            return Response(
                    {
                        "status":"error",
                        "message":"Invalid Credentials",
                       
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e :
            logger.critical(f"Unexpected Error in Login {str(e)}")
            
            return Response(
                {
                    "status":"error",
                    "messasge": "An unexpected error happend"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class Profile(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self,request):
        try :
            user = request.user
               
            user_data = {
                "id": user.id,
                "email": user.email,
                "name": user.name, 
                "profile_image": user.profile_image.url, 
            }
            return Response(
            {
                "status":'success',
                "message":'User Profile',
                "profile":user_data
                
            },
            status= status.HTTP_200_OK
        )
        except Exception as e:
            logger.critical(f"Unexpected Error {str(e)}")
            return Response (
                { 
                 "status":'Error',  
                 "message":"An unexpected error happend"
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        