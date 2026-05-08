from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    stock_qty = models.IntegerField()
    expiration_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Bread', 'Bread'),
        ('Pastry', 'Pastry'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_qty = models.IntegerField()
    baked_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="")
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_time = models.DateTimeField(auto_now_add=True)
    is_voided = models.BooleanField(default=False)

    def __str__(self):
        return f"Sale #{self.id} by {self.user.username} on {self.sale_time}"


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    is_voided = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} for Sale #{self.sale.id}"
