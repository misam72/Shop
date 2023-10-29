from django.db import models
from django.conf import settings
from home.models import Product

class Order(models.Model):
    ''' Note:
    For using the User model as foreign key we have 3 options:
    Opt 1:
    from account.models import User
    user = models.ForeignKey(User,...)
    Opt 2:
    from django.contrib.auth import get_user_model
    user = models.ForeignKey(get_user_model(),...)
    Opt 3:'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('paid', '-updated')
    
    def __str__(self):
        return f'{self.user} - {str(self.id)}'
    
    # A model-method. get the total price of all orders.
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return f'{self.id}'

    # A model-method
    def get_cost(self):
        return self.price * self.quantity
