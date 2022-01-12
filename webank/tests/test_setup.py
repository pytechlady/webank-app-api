from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
import testing.postgresql


class TestSetup(APITestCase):
    
    def setUp(self):   
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.create_account_url=reverse('create-account')
        self.faker = Faker()
        self.postgresql = testing.postgresql.Postgresql(port=7654)
        
        self.user_data={
            'email': self.faker.email(),
            'username': self.faker.email().split('@')[0],
            'password': self.faker.email(),
        }
        
        return super().setUp()
    
    def tearDown(self):
        return super().tearDown()