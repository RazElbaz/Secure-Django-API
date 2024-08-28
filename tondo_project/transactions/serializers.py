from rest_framework import serializers

class TransactionSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=100)
    date_time = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    sender = serializers.CharField(max_length=100)
    receiver = serializers.CharField(max_length=100)
    transaction_type = serializers.ChoiceField(choices=['purchase', 'sale', 'refund', 'transfer'])  # Adjust choices as needed
