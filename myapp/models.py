# myapp/models.py
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class MyUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=256)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.username