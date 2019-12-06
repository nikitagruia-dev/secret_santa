from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.common.models import BaseModel


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    password = None
    is_superuser = None
    username = None
    is_staff = None
    first_name = None
    last_name = None
    last_login = None
    is_active = None

    email = models.EmailField(max_length=254, verbose_name='email address', unique=True)
    selected = models.BooleanField(default=False)
    chat_id = models.IntegerField(null=True)
    name = models.CharField(max_length=150, null=True)
    santa_notified = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    token = models.CharField(max_length=50, null=True)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __str__(self):
        return f'{self.email} {self.name}'


class Santa(BaseModel):
    santa = models.ForeignKey(User, on_delete=models.CASCADE, related_name='santa')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='santa_target')
