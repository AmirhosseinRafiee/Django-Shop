from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CartModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

    def get_cart_total_price(self):
        total = 0
        for item in self.cartitemmodel_set.all():
            total += item.product.get_price() * item.quantity
        return total

class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel,on_delete=models.CASCADE)
    product = models.ForeignKey('shop.ProductModel',on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - {self.cart.id}"

    def get_total_price(self):
        return self.quantity * self.product.get_price()
