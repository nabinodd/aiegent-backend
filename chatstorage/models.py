import json

from django.db import models

from server_aiegent.models import TimestampedModel


class ChatMessage(TimestampedModel):
    sender = models.CharField(max_length=50)
    message = models.JSONField()

    def __str__(self):
        preview = json.dumps(self.message, ensure_ascii=False)[:80]
        return f"{self.sender}: {preview}"
