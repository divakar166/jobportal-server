from django.urls import path
from .views import AddJobView, JobListingView, JobListingRecruiterView, JobListingRecruiterCountView

urlpatterns = [
  path('add-job', AddJobView.as_view(), name="add-job"),
  path('', JobListingView.as_view(), name="jobs"),
  path('recruiter', JobListingRecruiterView.as_view(), name="jobs-recruiter"),
  path('recruiter/count', JobListingRecruiterCountView.as_view(), name="jobs-recruiter-count")
]