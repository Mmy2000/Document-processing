from django.contrib import admin
from .models import UploadedFile, ImageDetails, PDFDetails
# Register your models here.

admin.site.register(UploadedFile)
admin.site.register(ImageDetails)
admin.site.register(PDFDetails)