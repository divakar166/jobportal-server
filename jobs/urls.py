from django.urls import path
from .views import AddJobView

urlpatterns = [
  path('add-job', AddJobView.as_view(), name="add-job")
]