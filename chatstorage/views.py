from django.db import transaction
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatMessage


def _normalize_payload(data: dict) -> dict:

    if isinstance(data, dict) and "received" in data and isinstance(data["received"], dict):
        return data["received"]
    return data


def _extract_sender(received: dict) -> str | None:
    try:
        if "messages" in received and received["messages"]:
            frm = received["messages"][0].get("from")
            if frm:
                return frm
    except Exception:
        pass
    return None


class ChatDataAPIView(APIView):
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        incoming = request.data
        received = _normalize_payload(incoming)

        sender = _extract_sender(received)
        if not sender:
            return Response(
                {"detail": "Could not determine sender (wa_id / from missing)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        obj = ChatMessage.objects.create(sender=sender, message=received)
        return Response(
            {
                "id": str(obj.pk),
                "sender": obj.sender,
                "stored": True,
            },
            status=status.HTTP_201_CREATED,
        )
