from django.db import models
import uuid
from django.utils.timezone import now
from recruiter.models import Recruiter

class JobListing(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name="jobs")
  
  job_title = models.CharField(max_length=255)
  job_type = models.CharField(max_length=50, choices=[
    ('full_time', 'Full-Time'),
    ('part_time', 'Part-Time'),
    ('internship', 'Internship')
  ])
  
  job_location = models.CharField(max_length=255, choices=[
    ('onsite', 'On-Site'),
    ('remote', 'Remote'),
    ('hybrid', 'Hybrid')
  ])
  company_name = models.CharField(max_length=255)
  location = models.CharField(max_length=255)
  
  experience = models.CharField(max_length=100)
  skills = models.TextField()
  salary = models.CharField(max_length=100)
  
  start_date = models.DateField(null=True, blank=True)
  apply_by = models.DateField(null=True, blank=True)

  openings = models.PositiveIntegerField(default=1)
  about = models.TextField()

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    db_table = "job_listings"
    ordering = ["-created_at"]

  def __str__(self):
    return f"{self.job_title} at {self.company_name}"
