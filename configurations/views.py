from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AllowedNumber


class CheckAccessAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response(
                {"error": "phone_number is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        number = AllowedNumber.objects.filter(number=phone_number)
        if number.exists():
            if number.first().is_allowed:
                return Response(
                    {"allowed": True},
                    status=status.HTTP_200_OK
                )

        return Response(
            {"allowed": False},
            status=status.HTTP_200_OK
        )
