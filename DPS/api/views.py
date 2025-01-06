from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import Base64FileSerializer , UploadedFileSerializer, ImageDetailsSerializer, PDFDetailsSerializer
from .models import UploadedFile, ImageDetails, PDFDetails
from django.shortcuts import get_object_or_404
import os
from PIL import Image
from django.http import FileResponse
import io
import base64
from pdf2image import convert_from_bytes
import uuid
from django.conf import settings
from pdf2image import convert_from_path
from rest_framework.exceptions import NotFound

# Create your views here.

class UploadFileView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = Base64FileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.save()
            return Response(
                {
                    "id": uploaded_file.id,
                    "file_type": uploaded_file.file_type,
                    "file_path": uploaded_file.file_path.url,  # Adjust if using a file system
                    "uploaded_at": uploaded_file.uploaded_at,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FileListView(APIView):
    def get(self, request, file_type):
        files = UploadedFile.objects.filter(file_type=file_type)
        return Response(UploadedFileSerializer(files, many=True,context={'request':request}).data)

class FileDetailView(APIView):
    def get(self, request, file_type, pk):
        file = get_object_or_404(UploadedFile, pk=pk, file_type=file_type)
        if file_type == 'image':
            details = get_object_or_404(ImageDetails, file=file)
            serializer = ImageDetailsSerializer(details,context={'request':request})
        elif file_type == 'pdf':
            details = get_object_or_404(PDFDetails, file=file)
            serializer = PDFDetailsSerializer(details,context={'request':request})
        return Response(serializer.data)

    def delete(self, request, file_type, pk):
        file = get_object_or_404(UploadedFile, pk=pk, file_type=file_type)
        print(file.file_path.path)
        os.remove(file.file_path.path)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={"message": "File deleted successfully"})
    
class RotateImageView(APIView):
    def post(self, request):
        file_id = request.data.get('file_id')
        angle = request.data.get('angle')

        if not file_id or angle is None:
            return Response({'error': 'file_id and angle are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the file object
            file = get_object_or_404(UploadedFile, pk=file_id, file_type='image')

            # Open the image file and rotate it
            with Image.open(file.file_path.path) as img:
                rotated_img = img.rotate(float(angle), expand=True)
                buffer = io.BytesIO()
                rotated_img.save(buffer, format='PNG')
                buffer.seek(0)

            # Return the rotated image as a response
            return FileResponse(buffer, content_type='image/png')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ConvertPDFToImageView(APIView):
    def post(self, request):
        pdf_id = request.data.get("pdf_id")
        if not pdf_id:
            return Response({"error": "PDF ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uploaded_file = UploadedFile.objects.get(id=pdf_id, file_type="pdf")
        except UploadedFile.DoesNotExist:
            return Response({"error": "PDF not found."}, status=status.HTTP_404_NOT_FOUND)

        pdf_path = uploaded_file.file_path.path
        if not os.path.exists(pdf_path):
            return Response({"error": "File not found on server."}, status=status.HTTP_404_NOT_FOUND)

        try:
            images = convert_from_path(pdf_path, dpi=200)
            image_urls = []

            for i, image in enumerate(images):
                image_name = f"{uuid.uuid4().hex}_page_{i + 1}.png"
                image_path = os.path.join(settings.MEDIA_ROOT, "uploads", image_name)
                os.makedirs(os.path.dirname(image_path), exist_ok=True)
                image.save(image_path, "PNG")

                relative_image_path = os.path.join("uploads", image_name)
                image_urls.append(request.build_absolute_uri(settings.MEDIA_URL + relative_image_path))

            return Response({"images": image_urls}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Failed to convert PDF: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
