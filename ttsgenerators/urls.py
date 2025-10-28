from django.urls import path

from .views import TextToSpeechAPIView

urlpatterns = [
    path('tts-generate/', TextToSpeechAPIView.as_view(), name='tts-generate'),
]