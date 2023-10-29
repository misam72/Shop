from django.db import models
from django.conf import settings

class Order(models.Model):
    # For using the User model as foreign key we have 3 options:
    # Opt 1:
    # from account.models import User
    # user = models.ForeignKey(User,...)
    # Opt 2:
    # from django.contrib.auth import get_user_model
    # user = models.ForeignKey(get_user_model(),...)
    # Opt 3:
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class OrderItem(models.Model):
    ...
