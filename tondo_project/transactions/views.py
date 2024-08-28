from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
import random
import uuid
from faker import Faker
import logging
from .serializers import TransactionSerializer

logger = logging.getLogger(__name__)
fake = Faker() # initialize Faker

USER_ROLES = {
    "b4d3658f-8c48-4e63-9f77-09dbb0a7d55e": ["admin"],
    "f2d9e912-df15-4d5e-9c7d-f72d08c5d351": ["user"],
    "92d9e13e-9d4d-4a91-8e3d-37e8c92a2f70": ["superuser"],
    "e1c4b3f7-9a8c-4d8b-99f0-b5d8d079c256": ["editor"],
    "9f6e72c3-40c8-42cb-bf2a-8c56f3b672d5": ["viewer"],
    "5e86355d-9e89-4a67-9f28-77e748e2c5c5": ["admin", "user"],
    "21d7f3c8-b9ae-485e-964e-08b7899e6b6c": ["editor", "viewer"]
}

def get_user_roles(user_id):
    return USER_ROLES.get(user_id, [])

def create_dummy_transaction():
    """Creates a dummy transaction using Faker."""
    transaction = {
        "transaction_id": str(uuid.uuid4()),  
        "date_time": fake.date_time_between(start_date='-1y', end_date='now').strftime("%Y-%m-%d %H:%M:%S"),
        "currency": random.choice(['USD', 'EUR', 'GBP', 'JPY', 'INR']), 
        "sender": fake.name(),  
        "receiver": fake.name(), 
        "transaction_type": random.choice(['purchase', 'sale', 'refund', 'transfer']), 
    }
    return transaction
class GetDetails(APIView):
    def get(self, request):
        user_id = request.headers.get('userid')
        user_roles = get_user_roles(user_id)


        if 'admin' in user_roles or 'user' in user_roles:
            transaction = create_dummy_transaction()
            return Response(transaction, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
class SaveDetaile(APIView):
    def post(self, request):
        user_id = request.headers.get('userid')
        user_roles = get_user_roles(user_id)
        
        if 'admin' in user_roles:
            transaction = {
                "transaction_id": request.data.get('transaction_id'),  
                "date_time": request.data.get('date_time'), 
                "currency": request.data.get('currency'),
                "sender": request.data.get('sender'), 
                "receiver": request.data.get('receiver'), 
                "transaction_type": request.data.get('transaction_type'), 
            }

            serializer = TransactionSerializer(data = transaction)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)