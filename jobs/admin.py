from django.contrib import admin
from .models import JobListing

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
  list_display = ("job_title", "company_name", "job_type", "job_location", "apply_by", "created_at")
  search_fields = ("job_title", "company_name", "location", "skills")
  list_filter = ("job_type", "job_location", "created_at")
