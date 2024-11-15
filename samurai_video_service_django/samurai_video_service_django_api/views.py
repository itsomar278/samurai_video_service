from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VideoTranslation

class VideoTranslationStatusView(APIView):
    def get(self, request):
        request_id = request.query_params.get('request_id')

        if not request_id:
            return Response({"error": "Request ID is required as a query parameter."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            translation = VideoTranslation.objects.get(request_id=request_id)
            return Response({
                "request_id": str(translation.request_id),
                "status": translation.get_status_display(),
            }, status=status.HTTP_200_OK)
        except VideoTranslation.DoesNotExist:
            return Response({"error": "Translation request not found."}, status=status.HTTP_404_NOT_FOUND)

class VideoTranslationByUserView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response({"error": "User ID is required as a query parameter."},
                             status=status.HTTP_400_BAD_REQUEST)

        translations = VideoTranslation.objects.filter(user_id=user_id)

        if not translations.exists():
            return Response({"error": "No translations found for this user."},
                             status=status.HTTP_404_NOT_FOUND)

        translation_data = [
            {
                "request_id": str(translation.request_id),
                "status": translation.get_status_display(),
                "video_url": translation.video_url,
                "start_minute": translation.start_minute,
                "end_minute": translation.end_minute,
            }
            for translation in translations
        ]

        return Response({"translations": translation_data}, status=status.HTTP_200_OK)
