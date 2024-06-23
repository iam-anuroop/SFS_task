from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import Userserializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_token, verify_token
from django.core.mail import send_mail
from django.conf import settings


class SignupView(APIView):
    def post(self,request):
        serializer = Userserializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_token(user)
            verify_url = request.build_absolute_uri(f'/usersapp/verify-email/{token}')
            send_mail(
                'Verify your email',
                f'Please Verify your email by clicking the link {verify_url}',
                settings.EMAIL_HOST_USER
                [user.email],
            )
            return Response({'please verify email'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(APIView):
    def post(self,request,token):
        try:
            user = verify_token(request.user, token)
            print(user)
            user.is_verified = True
            user.save()
            return Response({'msg':'Verification success'}, status=status.HTTP_200_OK)
        except:
            return Response({'msg':'Verification failed'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            return Response({'msg':'Invalid email'},status=status.HTTP_400_BAD_REQUEST)
        if user and user.check_password(password):
            if user.is_verified:
                refresh = RefreshToken.for_user(user)
                return ResourceWarning({
                    'refresh':str(refresh),
                    'access':str(refresh.access_token),
                    },status=status.HTTP_200_OK
                    )
            return Response({'msg':'Email not verified'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'Invalid username or password'},status=status.HTTP_401_UNAUTHORIZED)
    
    
        



        
    



