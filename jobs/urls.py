from django.urls import path
from .views import *

urlpatterns = [
  path('add-job', AddJobView.as_view(), name="add-job"),
  path('', JobListingView.as_view(), name="jobs"),
  path('recruiter', JobListingRecruiterView.as_view(), name="jobs-recruiter"),
  path('recruiter/count', JobListingRecruiterCountView.as_view(), name="jobs-recruiter-count"),
  path('<uuid:job_id>/delete/', DeleteJobView.as_view(), name='delete-job'),
  path('<uuid:job_id>/update/', EditJobView.as_view(), name='edit-job')
]