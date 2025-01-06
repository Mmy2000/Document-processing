from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import Base64FileSerializer , UploadedFileSerializer, ImageDetailsSerializer, PDFDetailsSerializer
from .models import UploadedFile, ImageDetails, PDFDetails
from django.shortcuts import get_object_or_404
import os

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
        return Response(UploadedFileSerializer(files, many=True).data)

class FileDetailView(APIView):
    def get(self, request, file_type, pk):
        file = get_object_or_404(UploadedFile, pk=pk, file_type=file_type)
        if file_type == 'image':
            details = get_object_or_404(ImageDetails, file=file)
            serializer = ImageDetailsSerializer(details)
        elif file_type == 'pdf':
            details = get_object_or_404(PDFDetails, file=file)
            serializer = PDFDetailsSerializer(details)
        return Response(serializer.data)

    def delete(self, request, file_type, pk):
        file = get_object_or_404(UploadedFile, pk=pk, file_type=file_type)
        print(file.file_path.path)
        os.remove(file.file_path.path)
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={"message": "File deleted successfully"})