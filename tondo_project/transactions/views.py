from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from faker import Faker
import logging
from .serializers import TransactionSerializer
from .services.cerbos_client import check_user_role
from .services.user_roles import get_user_roles
import requests
from .models import Transaction

logger = logging.getLogger(__name__)

class GetDetails(APIView):
    def get(self, request):
        user_id = request.headers.get('userid')
        if not user_id:
            return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_roles = get_user_roles(user_id)

        logger.info(f"GetDetails request by user_id: {user_id} with roles: {user_roles}")

        if check_user_role(user_id, 'get_details'):
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
            serializer = TransactionSerializer(data = request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)