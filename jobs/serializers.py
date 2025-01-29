from rest_framework import serializers
from jobs.models import JobListing

class JobListingSerializer(serializers.ModelSerializer):
  class Meta:
    model = JobListing
    fields = "__all__"

  def validate(self, data):
    """Custom validation to ensure `apply_by` date is after `start_date`."""
    start_date = data.get("start_date")
    apply_by = data.get("apply_by")

    if start_date and apply_by and apply_by <= start_date:
      raise serializers.ValidationError({"apply_by": "Apply by date must be after the start date."})

    return data