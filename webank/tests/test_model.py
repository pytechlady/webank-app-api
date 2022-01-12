from django.http import response
from .test_setup import TestSetup
from django.urls import reverse
from ..models import AccountManager, Balance, TransactionHistory, User


class TestModel(TestSetup):
    def test_model_list(self):
        response = self.client.get('model_list')
        self.assertNotEqual(response.status_code, 400)
        
    def test_model_detail(self):
        models = User.object.all()
        if models:
            response = self.client.get(reverse('model-detail', args=[models[0].id]))
            self.assertEqual(response.status_code, 200)
            
    def test_account_model_detail(self):
        models = AccountManager.objects.all()
        if models:
            response = self.client.get(reverse('model-detail', args=[models[0].account_number]))
            self.assertEqual(response.status_code, 200)
            
    def test_balance_model_detail(self):
        models = Balance.objects.all()
        if models:
            response = self.client.get(reverse('model-detail', args=[models[0].customer]))
            self.assertEqual(response.status_code, 200)
            
    def test_transaction_model_detail(self):
        models = TransactionHistory.objects.all()
        if models:
            response = self.client.get(reverse('model-detail', args=[models[0].user_id]))
            self.assertEqual(response.status_code, 200)