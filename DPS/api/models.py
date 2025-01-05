import uuid
from django.db import models


class UploadedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FILE_TYPES = [("image", "Image"), ("pdf", "PDF")]
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file_path = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_path.name


class ImageDetails(models.Model):
    file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE)
    width = models.IntegerField()
    height = models.IntegerField()
    channels = models.IntegerField()

    def __str__(self):
        return f"{self.width}x{self.height}x{self.channels}"


class PDFDetails(models.Model):
    file = models.OneToOneField(UploadedFile, on_delete=models.CASCADE)
    pages = models.IntegerField()
    page_width = models.FloatField()
    page_height = models.FloatField()

    def __str__(self):
        return f"{self.pages} pages"
