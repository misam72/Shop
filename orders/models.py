from django.db import models
from django.conf import settings
from home.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

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
    discount = models.IntegerField(blank=True, null=True, default=None)
    
    class Meta:
        ordering = ('paid', '-updated')
    
    def __str__(self):
        return f'{self.user} - {str(self.id)}'
    
    # A model-method. get the total price of all orders.
    def get_total_price(self):
        total_price = sum(item.get_cost() for item in self.items.all())
        if self.discount:
            discount_price = (self.discount / 100) * total_price
            return float(total_price - discount_price)
        else:
            return total_price


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


class Coupon(models.Model):
    code = models.CharField(max_length=30, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)])
    active = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.code}'
    
