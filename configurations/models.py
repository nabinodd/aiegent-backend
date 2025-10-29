from django.db import models

from server_aiegent.models import TimestampedModel


class AllowedNumber(TimestampedModel):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)
    is_allowed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.number
