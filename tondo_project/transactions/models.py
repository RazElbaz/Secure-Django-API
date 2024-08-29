from django.db import models
import uuid

class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_time = models.DateTimeField()
    currency = models.CharField(max_length=10)
    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    transaction_type = models.CharField(max_length=50)


    def __str__(self):
        return f"Transaction {self.transaction_id} by {self.sender} to {self.receiver}"
