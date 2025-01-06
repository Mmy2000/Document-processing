# Document Processing API

Welcome to the Document Processing API! This application allows users to upload and process image and PDF files with a range of features, including rotating images, converting PDFs to images, and more.

---

## Features

### Upload and Retrieve Files
- **`POST /api/upload/`**: Accepts image and PDF files in Base64 format and saves them to the server.
- **`GET /api/image/`**: Returns a list of all uploaded images.
- **`GET /api/pdf/`**: Returns a list of all uploaded PDFs.

### File Details
- **`GET /api/image/{id}/`**: Returns details of a specific image (location, dimensions, channels).
- **`GET /api/pdf/{id}/`**: Returns details of a specific PDF (location, number of pages, dimensions).

### File Operations
- **`DELETE /api/image/{id}/`**: Deletes a specific image.
- **`DELETE /api/pdf/{id}/`**: Deletes a specific PDF.
- **`POST /api/rotate/rotate/`**: Rotates an image by a specified angle.
- **`POST /api/convert/convert-pdf-to-image/`**: Converts a PDF to an image.
---

## Requirements

- **Backend Framework**: Django, Django Rest Framework (DRF)
- **Database**: SQLite (default, can be updated)
- **Deployment**: Dockerized for easy deployment

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd project-name

## URLS
  - **url documentaion** : https://documenter.getpostman.com/view/31929307/2sAYJ9BecZ
  - **url website in pythonanywhere** : https://dpservice.pythonanywhere.com

