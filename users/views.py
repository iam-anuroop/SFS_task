from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from .serializers import Userserializer
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_token, verify_token
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import check_password


class SignupView(APIView):
    def post(self,request):
        serializer = Userserializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_token(user)
            verify_url = request.build_absolute_uri(f'/usersapp/verify-email/{token}/')
            mail_subject = "Verify"
            message = f'click this url to verify your email, {verify_url}'
            to_email = user.email
            send_mail = EmailMessage(mail_subject, message, to=[to_email])
            send_mail.send()

            return Response({'please verify email'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(APIView):
    def get(self,request,token):
        try:
            user = verify_token(token)
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
        if user is not None and check_password(password,user.password):
            if user.is_verified:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh':str(refresh),
                    'access':str(refresh.access_token),
                    },status=status.HTTP_200_OK
                    )
            return Response({'msg':'Email not verified'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'Invalid username or password'},status=status.HTTP_401_UNAUTHORIZED)
    
    
        



        
    



