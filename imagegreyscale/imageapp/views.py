# imageapp/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from PIL import Image, ImageOps
from io import BytesIO
from .models import UploadedImage
from .serializers import UploadedImageSerializer
import base64


class UploadImageView(APIView):
    def post(self, request, *args, **kwargs):
        image_serializer = UploadedImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            image_instance = UploadedImage.objects.last()
            grayscale_image = self.convert_to_grayscale(image_instance.image)
            return Response(
                {
                    "message": "Image uploaded and converted to grayscale.",
                    "grayscale_image": grayscale_image,
                },
                status=status.HTTP_200_OK,
            )
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        image_instance = UploadedImage.objects.last()
        if image_instance:
            grayscale_image = self.convert_to_grayscale(image_instance.image)
            response = Response(
                {
                    "message": "Grayscale image retrieved.",
                    "grayscale_image": grayscale_image,
                },
                status=status.HTTP_200_OK,
            )
            self.add_cors_headers(response)
            return response
        else:
            return Response(
                {"error": "No uploaded image found."}, status=status.HTTP_404_NOT_FOUND
            )

    def add_cors_headers(self, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"

    def convert_to_grayscale(self, image):
        img_obj = Image.open(image)
        grayscale_image = ImageOps.grayscale(img_obj)
        bytesio = BytesIO()
        grayscale_image.save(bytesio, format="PNG")
        base64_image = base64.b64encode(bytesio.getvalue()).decode("utf-8")
        return base64_image
