from django.urls import path

from .views import ChatDataAPIView

urlpatterns = [
    path('chat-data/', ChatDataAPIView.as_view(), name='chat-data'),
]
