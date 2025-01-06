from django.urls import path
from api.views import UploadFileView, FileListView, FileDetailView

urlpatterns = [
    path("upload/", UploadFileView.as_view(),name="upload_file"),
    path("<str:file_type>/", FileListView.as_view()),
    path("<str:file_type>/<uuid:pk>/", FileDetailView.as_view()),

]
