from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
import os

# Ensure you have a consistent encryption key
key = os.getenv('DJANGO_ENCRYPTION_KEY', Fernet.generate_key())
cipher_suite = Fernet(key)

class AWSCredential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_key_id = models.CharField(max_length=255)
    secret_access_key = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.access_key_id = cipher_suite.encrypt(self.access_key_id.encode()).decode()
        self.secret_access_key = cipher_suite.encrypt(self.secret_access_key.encode()).decode()
        super().save(*args, **kwargs)

    def get_access_key_id(self):
        return cipher_suite.decrypt(self.access_key_id.encode()).decode()

    def get_secret_access_key(self):
        return cipher_suite.decrypt(self.secret_access_key.encode()).decode()

