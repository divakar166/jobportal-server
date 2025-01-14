from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.utils import timezone
from .serializers import DeveloperSerializer
from .models import Developer, VerificationToken
from .utils import send_verification_email
import jwt
import datetime
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from .signals import developer_registered

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = DeveloperSerializer(data=request.data)
        if serializer.is_valid():
            developer = serializer.save()
            developer.set_password(developer.password)
            developer.save()

            # Generate verification token
            token = get_random_string(32)
            expires_at = timezone.now() + datetime.timedelta(hours=24)

            # Save verification token in the database
            VerificationToken.objects.create(
                email=developer.email,
                token=token,
                expires=expires_at,
            )

            developer_registered.send(
                sender=self.__class__,
                email=developer.email,
                token=token,
                role="developer"
            )

            return Response(
                {"message": "Registered successfully! Verification email sent."},
                status=status.HTTP_201_CREATED,
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            developer = Developer.objects.get(email=email)
        except Developer.DoesNotExist:
            return Response({"error": "User doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)

        if not developer.email_verified:
            verification_token = VerificationToken.objects.get(email=email)
            if verification_token.has_expired():
                verification_token.delete()
                token = get_random_string(32)
                expires_at = timezone.now() + datetime.timedelta(hours=24)
                VerificationToken.objects.create(
                    email=developer.email,
                    token=token,
                    expires=expires_at,
                )
                developer_registered.send(
                    sender=self.__class__,
                    email=developer.email,
                    token=token,
                    role="developer"
                )
            return Response({"error": "Verify email!"}, status=status.HTTP_403_FORBIDDEN)

        if not developer.check_password(password):
            return Response({"error": "Incorrect password!"}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            'id': str(developer.id),
            'email': developer.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = JsonResponse({
            'message': 'Login successful!',
            'token': token,
            'name': developer.name,
        })
        return response


class DeveloperVerifyToken(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            verification_token = VerificationToken.objects.filter(token=token).first()
            if not verification_token:
                return Response({"error": "Token does not exist!"}, status=status.HTTP_404_NOT_FOUND)

            if verification_token.has_expired():
                print("Token has expired!")
                return Response({"error": "Token has expired!"}, status=status.HTTP_400_BAD_REQUEST)

            developer = Developer.objects.filter(email=verification_token.email).first()
            if not developer:
                return Response({"error": "Developer not found!"}, status=status.HTTP_404_NOT_FOUND)

            developer.email_verified = True
            developer.save()

            verification_token.delete()

            return Response({"success": "Email successfully verified!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(
                {"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
