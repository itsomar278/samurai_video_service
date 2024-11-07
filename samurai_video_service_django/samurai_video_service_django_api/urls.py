from django.urls import path
from .views import VideoTranslationCreateView

urlpatterns = [
    path('video-transiclate/create/', VideoTranslationCreateView.as_view(), name='video-translation-create'),
]
