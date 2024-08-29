from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
import uuid
from faker import Faker
import logging
from .serializers import TransactionSerializer
from .user_roles import get_user_roles
import requests
from .models import Transaction

logger = logging.getLogger(__name__)
fake = Faker() # initialize Faker
CERBOS_URL = 'http://cerbos:3592/api/check'


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

def check_user_role(user_id, action):
    """Check if the user is authorized to perform the given action."""
    #https://docs.cerbos.dev/cerbos/latest/policies/scoped_policies
    roles = get_user_roles(user_id)
    payload = {
        "request_id": str(uuid.uuid4()), 
        "actions": [action],
        "principal": {
            "id": user_id,
            "roles": roles
        },
        "resource": {
            "kind": "transaction",  
            "instances": {
                "resource_id": {}
            }
        }
    }
    
    logger.info(payload)
    try:
        response = requests.post(CERBOS_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        # Check if the action is allowed, https://docs.cerbos.dev/cerbos/latest/tutorial/03_calling-cerbos.html
        actions = result.get("resourceInstances", {}).get("resource_id", {}).get('actions', {})
        action_effect = actions.get(action, 'EFFECT_DENY')

        if action_effect  == 'EFFECT_ALLOW':
            return True
    except requests.RequestException as e:
        logger.error(f"Error contacting Cerbos: {e}")
    
    return False
    
class GetDetails(APIView):
    def get(self, request):
        user_id = request.headers.get('userid')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_roles = get_user_roles(user_id)

        logger.info(f"GetDetails request by user_id: {user_id} with roles: {user_roles}")

        if check_user_role(user_id, 'get_details'):
            # transaction = create_dummy_transaction()
            transactions = Transaction.objects.all()
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data , status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        
class SaveDetails(APIView):
    def post(self, request):
        user_id = request.headers.get('userid')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_roles = get_user_roles(user_id)
        
        logger.info(f"SaveDetails request by user_id: {user_id} with roles: {user_roles}")

        if check_user_role(user_id, 'save_details'):
            transaction = {
                "transaction_id": request.data.get('transaction_id'),  
                "date_time": request.data.get('date_time'), 
                "currency": request.data.get('currency'),
                "sender": request.data.get('sender'), 
                "receiver": request.data.get('receiver'), 
                "transaction_type": request.data.get('transaction_type'), 
            }

            serializer = TransactionSerializer(data = request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)