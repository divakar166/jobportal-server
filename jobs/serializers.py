from rest_framework import serializers
from jobs.models import JobListing
from datetime import datetime

class JobListingSerializer(serializers.ModelSerializer):
  start_date = serializers.DateTimeField(format="%Y-%m-%d", input_formats=["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d"], required=False)
  apply_by = serializers.DateTimeField(format="%Y-%m-%d", input_formats=["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d"], required=False)
  class Meta:
    model = JobListing
    fields = "__all__"

  def validate(self, data):
    """Custom validation to ensure `apply_by` date is after `start_date`."""
    start_date = self._convert_date(data.get("start_date"))
    apply_by = self._convert_date(data.get("apply_by"))
    print(start_date, apply_by)

    if data["start_date"] and data["apply_by"] and data["apply_by"] <= data["start_date"]:
      raise serializers.ValidationError({"apply_by": "Apply by date must be after the start date."})

    return data

  def _convert_date(self, value):
    if isinstance(value, str):
      print("entered")
      try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()  # Converts ISO format
      except ValueError:
        try:
          return datetime.strptime(value, "%Y-%m-%d").date()  # Handles YYYY-MM-DD
        except ValueError:
          raise serializers.ValidationError(f"Invalid date format: {value}. Use YYYY-MM-DD.")

    return value