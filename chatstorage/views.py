from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ChatDataAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        received_data = request.data
        response_data = {"received": received_data}
        return Response(response_data, status=status.HTTP_201_CREATED)