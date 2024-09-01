from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
import json
from .services.utils import create_dummy_transaction
from .models import Transaction

class TransactionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.transaction_data = create_dummy_transaction()
        self.transaction = Transaction.objects.create(
            date_time=self.transaction_data['date_time'],
            currency=self.transaction_data['currency'],
            sender=self.transaction_data['sender'],
            receiver=self.transaction_data['receiver'],
            transaction_type=self.transaction_data['transaction_type']
        )

    def _test_get_details(self, user_id, expected_status, expected_count=1):
        response = self.client.get('/api/get_details', HTTP_USERID=user_id)
        self.assertEqual(response.status_code, expected_status)
        if expected_status == status.HTTP_200_OK:
            self.assertEqual(len(response.data), expected_count)

    def _test_save_details(self, user_id, data, expected_status):
        response = self.client.post('/api/save_details', data=json.dumps(data),
                                    content_type='application/json', HTTP_USERID=user_id)
        self.assertEqual(response.status_code, expected_status)

    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_get_details_role_access(self, mock_check_user_role, mock_get_user_roles):
        roles = ['admin', 'superuser', 'user', 'editor', 'viewer']
        expected_statuses = {
            'admin': status.HTTP_200_OK,
            'superuser': status.HTTP_200_OK,
            'user': status.HTTP_200_OK,
            'editor': status.HTTP_403_FORBIDDEN,
            'viewer': status.HTTP_403_FORBIDDEN
        }
        
        for role in roles:
            mock_get_user_roles.return_value = [role]
            mock_check_user_role.return_value = (role in ['admin', 'superuser', 'user'])
            self._test_get_details('mock_user_id', expected_statuses[role])

    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_save_details_role_access(self, mock_check_user_role, mock_get_user_roles):
        roles = ['admin', 'superuser', 'editor', 'viewer']
        expected_statuses = {
            'admin': status.HTTP_200_OK,
            'superuser': status.HTTP_200_OK,
            'editor': status.HTTP_403_FORBIDDEN,
            'viewer': status.HTTP_403_FORBIDDEN
        }
        
        for role in roles:
            mock_get_user_roles.return_value = [role]
            mock_check_user_role.return_value = (role in ['admin', 'superuser'])
            self._test_save_details('mock_user_id', self.transaction_data, expected_statuses[role])

    @patch('transactions.views.get_user_roles')
    def test_save_details_missing_userid(self, mock_get_user_roles):
        response = self.client.post('/api/save_details', data=json.dumps(self.transaction_data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'User ID is required')

    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_get_details_empty_database(self, mock_check_user_role, mock_get_user_roles):
        Transaction.objects.all().delete()  # clear out all transactions
        
        mock_get_user_roles.return_value = ['admin']
        mock_check_user_role.return_value = True
        self._test_get_details('mock_user_id', status.HTTP_200_OK, expected_count=0)

    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_save_details_invalid_data(self, mock_check_user_role, mock_get_user_roles):

        invalid_data = {
            'date_time': 'invalid_date',
            'currency': 'INVALID',
            'sender': '',
            'receiver': '',
            'transaction_type': 'invalid_type'
        }
        mock_get_user_roles.return_value = ['admin']
        mock_check_user_role.return_value = True
        self._test_save_details('mock_user_id', invalid_data, status.HTTP_400_BAD_REQUEST)

    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_save_details_missing_fields_sender_receiver(self, mock_check_user_role, mock_get_user_roles):
        # Test with missing fields
        missing_fields_data = {
            'date_time': self.transaction_data['date_time'],
            'currency': self.transaction_data['currency'],
            # 'sender' and 'receiver' are missing
            'transaction_type': self.transaction_data['transaction_type']
        }
        mock_get_user_roles.return_value = ['admin']
        mock_check_user_role.return_value = True
        self._test_save_details('mock_user_id', missing_fields_data, status.HTTP_400_BAD_REQUEST)

    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_save_details_missing_fields_date_time(self, mock_check_user_role, mock_get_user_roles):
        missing_data = {
            # 'date_time' is missing
            'currency': 'USD',
            'sender': 'Alice',
            'receiver': 'Bob',
            'transaction_type': 'transfer'
        }
        mock_get_user_roles.return_value = ['admin']
        mock_check_user_role.return_value = True
        response = self.client.post('/api/save_details', data=json.dumps(missing_data),
                                    content_type='application/json', HTTP_USERID='mock_user_id')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_save_details_invalid_data_types(self, mock_check_user_role, mock_get_user_roles):
        invalid_data = {
            'date_time': 12345, 
            'currency': 123, 
            'sender': True,  
            'receiver': ['List'], 
            'transaction_type': None 
        }
        mock_get_user_roles.return_value = ['admin']
        mock_check_user_role.return_value = True
        response = self.client.post('/api/save_details', data=json.dumps(invalid_data),
                                    content_type='application/json', HTTP_USERID='mock_user_id')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_get_details_correct_serialization(self, mock_check_user_role, mock_get_user_roles):
        mock_get_user_roles.return_value = ['admin']
        mock_check_user_role.return_value = True
        
        response = self.client.get('/api/get_details', HTTP_USERID='mock_user_id')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['sender'], self.transaction_data['sender'])
        self.assertEqual(response.data[0]['receiver'], self.transaction_data['receiver'])
        self.assertEqual(response.data[0]['currency'], self.transaction_data['currency'])
        self.assertEqual(response.data[0]['transaction_type'], self.transaction_data['transaction_type'])

    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_get_details_bad_userid(self, mock_check_user_role, mock_get_user_roles):
        bad_user_id = 'invalid_user_id'
        mock_get_user_roles.return_value = []  
        mock_check_user_role.return_value = False
        
        response = self.client.get('/api/get_details', HTTP_USERID=bad_user_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'Forbidden')

    @patch('transactions.views.get_user_roles')
    @patch('transactions.views.check_user_role')
    def test_save_details_bad_userid(self, mock_check_user_role, mock_get_user_roles):
        bad_user_id = 'b4d3658f-8c48-4e63-9f7'
        mock_get_user_roles.return_value = []  
        mock_check_user_role.return_value = False
        
        response = self.client.post('/api/save_details', data=json.dumps(self.transaction_data),
                                    content_type='application/json', HTTP_USERID=bad_user_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], 'Forbidden')

