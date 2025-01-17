from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecruiterSerializer
from .models import Recruiter
from django.http import JsonResponse

class RegisterView(APIView):
  authentication_classes = []
  permission_classes = []

  def post(self, request):
    serializer = RecruiterSerializer(data=request.data)
    if serializer.is_valid():
      recruiter = serializer.save()
      recruiter.set_password(recruiter.password)
      recruiter.save()

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
      recruiter = Recruiter.objects.get(email=email)
    except Recruiter.DoesNotExist:
      return Response({"error": "User doesn't exist!"}, status=status.HTTP_404_NOT_FOUND)

    if not recruiter.check_password(password):
        return Response({"error": "Incorrect password!"}, status=status.HTTP_401_UNAUTHORIZED)

    token = recruiter.generate_token()

    response = JsonResponse({
      'message': 'Login successful!',
      'token': token,
      'name': recruiter.name,
    })
    return response