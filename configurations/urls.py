from django.urls import path

from .views import CheckAccessAPIView

urlpatterns = [
    path('check-access/', CheckAccessAPIView.as_view(), name='check-access'),
]
