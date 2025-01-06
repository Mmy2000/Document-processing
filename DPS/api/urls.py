from django.urls import path
from api.views import UploadFileView, FileListView, FileDetailView, RotateImageView, ConvertPDFToImageView

urlpatterns = [
    path("upload/", UploadFileView.as_view(),name="upload_file"),
    path("<str:file_type>/", FileListView.as_view()),
    path("<str:file_type>/<uuid:pk>/", FileDetailView.as_view()),
    path("rotate/rotate/", RotateImageView.as_view(), name="rotate_image"),
    path("convert/convert-pdf-to-image/", ConvertPDFToImageView.as_view(), name="convert_pdf_to_image"),
]
