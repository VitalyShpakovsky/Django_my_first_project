from django.urls import path
from .views import handel_file_upload

app_name = 'requestdataapp'

urlpatterns = [
    path("upload/", handel_file_upload, name="file-upload"),
]