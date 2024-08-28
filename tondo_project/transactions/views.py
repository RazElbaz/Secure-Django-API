from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
import uuid
from faker import Faker
import logging
from .serializers import TransactionSerializer
from .user_roles import get_user_roles

logger = logging.getLogger(__name__)
fake = Faker() # initialize Faker


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

        logger.info(f"GetDetails request by user_id: {user_id} with roles: {user_roles}")

        if 'admin' in user_roles or 'user' in user_roles or 'superuser' in user_roles:
            transaction = create_dummy_transaction()
            return Response(transaction, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
class SaveDetaile(APIView):
    def post(self, request):
        user_id = request.headers.get('userid')
        user_roles = get_user_roles(user_id)
        
        logger.info(f"SaveDetails request by user_id: {user_id} with roles: {user_roles}")

        if 'admin' in user_roles or 'superuser' in user_roles:
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