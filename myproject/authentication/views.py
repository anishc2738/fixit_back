from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from google.oauth2 import id_token
from google.auth.transport import requests

from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken,TokenError
import os

class GoogleLoginView(APIView):

    def post(self, request):

        token = request.data.get("token")
        print(os.getenv("GOOGLE_CLIENT_ID"))
        if not token:
            print("no token")
            return Response(
                {"error": "token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify Google token
            google_user = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                os.getenv("GOOGLE_CLIENT_ID")
            )
            name = google_user.get("name")
            email = google_user.get("email")

            # Find existing user or create new user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": name
                }
            )

            # Create JWT tokens
            refresh = RefreshToken.for_user(user)
            response=Response({
                "message": "Login Successful",
                "access": str(refresh.access_token),
                "name": name,
                "email": email,
                "isStaff": user.is_staff,
            })
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=7*24*60*60
            )
            print("Refresh token cookie:", response.cookies.get("refresh_token"))
            return response
            
        except ValueError as e:
            print(e)
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

class TokenRefreshView(APIView):
    def post(self, request):
        token=request.COOKIES.get('refresh_token')

        if not token:
            return Response(
                {
                    'error':"unable to find refresh token in cookie"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh=RefreshToken(token)
            user_id=refresh["user_id"]
            user=User.objects.get(id=user_id)
            return Response({
                'access':str(refresh.access_token),
                'name':user.get_full_name() or user.username,
                'email':user.email,
                'isStaff':user.is_staff
            })
        except TokenError:
            return Response({
                'error':"expireed or unauthorized token"
            },
            status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    def post(self,request):
        response=Response(
            {'message':"Logout successful"},
            status=status.HTTP_200_OK
        )
        response.delete_cookie('refresh_token',samesite="Lax")
        return response

