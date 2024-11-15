from django.urls import path
from .views import VideoTranslationStatusView, VideoTranslationByUserView

urlpatterns = [
    path('transclation-status/', VideoTranslationStatusView.as_view(), name='transclation_status'),
    path('transclation-status-by-user-id/', VideoTranslationByUserView.as_view(), name='transclation_status_by_user_id'),
]
