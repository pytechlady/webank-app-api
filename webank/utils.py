from django.core.mail import EmailMessage
import random
from django.utils.crypto import get_random_string


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject = data['email_subject'], 
                             body = data['email_body'], to = [data['to_email']])
        email.send()
   
    @staticmethod
    def generate_otp(number):
        min_val = 10 ** (number - 1)
        max_val = (10 ** number) - 1
        otp = random.randint(min_val, max_val)
        return otp

    @staticmethod
    def generate_account_number():
        return get_random_string(10, allowed_chars='0123456789')
