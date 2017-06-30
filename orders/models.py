from django.db import models
from photos.models import Photo
from django.contrib.auth.models import User

class Order(models.Model):
    userid = models.ForeignKey(User)
    product = models.ForeignKey(Photo,related_name='order_items')


    def __str__(self):
        return 'Order {}'.format(self.id)
    def get_cost(self):
        return self.price * self.quantity

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
