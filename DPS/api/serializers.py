from rest_framework import serializers
from .models import UploadedFile, ImageDetails, PDFDetails
import uuid
import base64
import os
from django.conf import settings
from PyPDF2 import PdfReader
from PIL import Image

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = "__all__"


class ImageDetailsSerializer(serializers.ModelSerializer):
    file = UploadedFileSerializer()
    class Meta:
        model = ImageDetails
        fields = ["width", "height", "channels", "file"]


class PDFDetailsSerializer(serializers.ModelSerializer):
    file = UploadedFileSerializer()
    class Meta:
        model = PDFDetails
        fields = ["pages", "page_width", "page_height", "file"]

class Base64FileSerializer(serializers.ModelSerializer):
    file_data = serializers.CharField(write_only=True)

    class Meta:
        model = UploadedFile
        fields = ["file_type", "file_data"]

    def validate_file_data(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError(
                "File data must be a base64-encoded string."
            )
        try:
            header, data = value.split(";base64,")
        except ValueError:
            raise serializers.ValidationError("Invalid base64 format.")
        return data

    def create(self, validated_data):
        file_type = validated_data.get("file_type")
        file_data = validated_data.get("file_data")
        decoded_file = base64.b64decode(file_data)

        # Determine the file extension
        if file_type == "image":
            file_ext = ".png"
        elif file_type == "pdf":
            file_ext = ".pdf"
        else:
            raise serializers.ValidationError("Unsupported file type.")

        # Generate file paths
        file_name = f"{uuid.uuid4().hex}{file_ext}"
        relative_path = f"uploads/{file_name}"
        absolute_path = os.path.join(settings.MEDIA_ROOT, relative_path)

        # Save the file to the server
        os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
        with open(absolute_path, "wb") as f:
            f.write(decoded_file)

        # Create UploadedFile instance
        uploaded_file = UploadedFile.objects.create(
            file_type=file_type, file_path=relative_path
        )

        # Process and save additional details based on file type
        if file_type == "image":
            self._save_image_details(uploaded_file, absolute_path)
        elif file_type == "pdf":
            self._save_pdf_details(uploaded_file, absolute_path)

        return uploaded_file

    def _save_image_details(self, uploaded_file, file_path):
        try:
            # Open the image file
            with Image.open(file_path) as img:
                width, height = img.size
                mode = img.mode  # Mode determines the channels
                
                # Determine channels based on mode
                mode_to_channels = {
                    "1": 1,    # 1-bit pixels, black and white
                    "L": 1,    # 8-bit pixels, grayscale
                    "P": 1,    # 8-bit pixels, mapped to palette
                    "RGB": 3,  # 3 channels (Red, Green, Blue)
                    "RGBA": 4, # 4 channels (Red, Green, Blue, Alpha)
                    "CMYK": 4, # 4 channels (Cyan, Magenta, Yellow, Black)
                }
                channels = mode_to_channels.get(mode, None)

                if channels is None:
                    raise ValueError(f"Unsupported image mode: {mode}")

                # Save image details to the database
                ImageDetails.objects.create(
                    file=uploaded_file, width=width, height=height, channels=channels
                )
        except Exception as e:
            raise serializers.ValidationError(f"Error processing image: {str(e)}")

    def _save_pdf_details(self, uploaded_file, file_path):
        try:
            # Extract PDF details
            pdf_reader = PdfReader(file_path)
            pages = len(pdf_reader.pages)
            first_page = pdf_reader.pages[0]
            page_width = first_page.mediabox.width
            page_height = first_page.mediabox.height
            PDFDetails.objects.create(
                file=uploaded_file,
                pages=pages,
                page_width=page_width,
                page_height=page_height,
            )
        except Exception as e:
            raise serializers.ValidationError(f"Error processing PDF: {str(e)}")
