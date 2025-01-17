from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DeveloperSerializer
from .models import Developer
from django.http import JsonResponse

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = DeveloperSerializer(data=request.data)
        if serializer.is_valid():
            developer = serializer.save()
            developer.set_password(developer.password)
            developer.save()

            return Response(
                {"message": "Registered successfully!"},
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

        if not developer.check_password(password):
            return Response({"error": "Incorrect password!"}, status=status.HTTP_401_UNAUTHORIZED)

        token = developer.generate_token()

        response = JsonResponse({
            'message': 'Login successful!',
            'token': token,
            'name': developer.name,
        })
        return response
