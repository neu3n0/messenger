from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.conf import settings

class CustomTokenObtainPairView(APIView):
    """
    View for login: checks credentials, generates JWT pair and sets tokens in httpOnly cookies.
    """

    permission_classes = []  # Access without authentication

    def post(self, request, *args, **kwargs):
        serializer = TokenObtainPairSerializer(data=request.data)

        if serializer.is_valid():
            tokens = serializer.validated_data  # Contains 'access' and 'refresh'
            response = Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
            # Set access-token in httpOnly cookie
            response.set_cookie(
                key='access_token',
                value=tokens.get('access'),
                httponly=True,
                secure=not settings.DEBUG,  # prod: use HTTPS
                samesite='Lax',
                max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
            )
            # Set refresh-token in httpOnly cookie
            response.set_cookie(
                key='refresh_token',
                value=tokens.get('refresh'),
                httponly=True,
                secure=not settings.DEBUG, # prod: use HTTPS
                samesite='Lax',
                max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenRefreshView(APIView):
    """
    View to refresh token: retrieves refresh token from httpOnly cookies, generates a new access-token 
    (and, if necessary, a new refresh-token), and sets them in the cookies.
    """
    permission_classes = []  # Access without authentication

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        tokens = serializer.validated_data  # New access-token and maybe new refresh-roken
        response = Response({'detail': 'Token refreshed successfully.'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=tokens.get('access'),
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            max_age=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
        )
        if 'refresh' in tokens:
            response.set_cookie(
                key='refresh_token',
                value=tokens.get('refresh'),
                httponly=True,
                secure=not settings.DEBUG,
                samesite='Lax',
                max_age=int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()),
            )
        return response
    
class LogoutView(APIView):
    """
    Logout view
    """
    permission_classes = []
    def post(self, request, *args, **kwargs):
        response = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response