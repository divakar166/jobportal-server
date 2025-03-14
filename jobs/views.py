from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt
from django.conf import settings
from jobs.models import JobListing
from jobs.serializers import JobListingSerializer, JobListingRecruiterSerializer, PartialJobListingSerializer
from django.shortcuts import get_object_or_404
from uuid import UUID
from django.utils.timezone import now

class AddJobView(APIView):
  authentication_classes = []
  permission_classes = []
  def post(self, request):
    token = request.headers.get("Authorization")
    if not token:
      return Response({"error": "Authentication token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    print(request.data.get("start_date"))
    try:
      decoded_token = jwt.decode(token.split(" ")[1], settings.SECRET_KEY, algorithms=["HS256"])
      recruiter_id = decoded_token.get("id")
    except jwt.ExpiredSignatureError:
      return Response({"error": "Token expired!"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
      return Response({"error": "Invalid token!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    request.data["recruiter"] = recruiter_id
    serializer = JobListingSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({"message": "Job added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobListingView(APIView):
  authentication_classes = []
  permission_classes = []
  def get(self, request):
    jobs = JobListing.objects.all()
    serializer = JobListingSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class JobListingRecruiterView(APIView):
  authentication_classes = []
  permission_classes = []
  def get(self, request):
    token = request.headers.get("Authorization")
    if not token:
      return Response({"error": "Authentication token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
      decoded_token = jwt.decode(token.split(" ")[1], settings.SECRET_KEY, algorithms=["HS256"])
      recruiter_id = decoded_token.get("id")
    except jwt.ExpiredSignatureError:
      return Response({"error": "Token expired!"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
      return Response({"error": "Invalid token!"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    jobs = JobListing.objects.filter(recruiter=recruiter_id)
    serializer = JobListingRecruiterSerializer(jobs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
class JobListingRecruiterCountView(APIView):
  authentication_classes = []
  permission_classes = []

  def get(self, request):
    token = request.headers.get("Authorization")
    if not token:
      return Response({"error": "Authentication token is required"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
      decoded_token = jwt.decode(token.split(" ")[1], settings.SECRET_KEY, algorithms=["HS256"])
      recruiter_id = decoded_token.get("id")

      # Fetch job listings for this recruiter
      job_listings = JobListing.objects.filter(recruiter=recruiter_id)
      total_count = job_listings.count()

      # Classify jobs as active or expired based on apply_by date
      active_count = job_listings.filter(apply_by__gte=now().date()).count()
      expired_count = job_listings.filter(apply_by__lt=now().date()).count()

      return Response(
        {"total": total_count, "active": active_count, "expired": expired_count},
        status=status.HTTP_200_OK
      )
    except jwt.ExpiredSignatureError:
      return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
      return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

class DeleteJobView(APIView):
  authentication_classes = []
  permission_classes = []
  
  def delete(self, request, job_id):
    token = request.headers.get("Authorization")
    if not token:
      return Response({"error": "Authentication token is required"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
      decoded_token = jwt.decode(token.split(" ")[1], settings.SECRET_KEY, algorithms=["HS256"])
      recruiter_id = decoded_token.get("id")
    except jwt.ExpiredSignatureError:
      return Response({"error": "Token expired!"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
      return Response({"error": "Invalid token!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
      job = JobListing.objects.get(id=job_id, recruiter=recruiter_id)
    except JobListing.DoesNotExist:
      return Response({"error": "Job not found or unauthorized access"}, status=status.HTTP_404_NOT_FOUND)
    
    job.delete()
    return Response({"message": "Job deleted successfully!"}, status=status.HTTP_200_OK)
  
class EditJobView(APIView):
  authentication_classes = []
  permission_classes = []

  def patch(self, request, job_id):
    token = request.headers.get("Authorization")
    if not token:
      return Response({"error": "Authentication token is required"}, status=status.HTTP_401_UNAUTHORIZED)
      
    try:
      decoded_token = jwt.decode(token.split(" ")[1], settings.SECRET_KEY, algorithms=["HS256"])
      recruiter_id = UUID(decoded_token.get("id"))
    except jwt.ExpiredSignatureError:
      return Response({"error": "Token expired!"}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
      return Response({"error": "Invalid token!"}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
      job = get_object_or_404(JobListing, id=job_id)

      if job.recruiter.id != recruiter_id:
          return Response({"error": "You do not have permission to edit this job."}, status=status.HTTP_403_FORBIDDEN)

      serializer = PartialJobListingSerializer(job, data=request.data, partial=True)  # Partial update
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
      
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    except Exception as e:
      return Response({"message": "Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)