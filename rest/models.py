from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

class Category(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    category = models.ForeignKey(
        Category, 
        related_name='products',
        on_delete=models.SET_NULL,
        null=True
    )
    is_available = models.BooleanField(default=True)
    preparation_time = models.PositiveIntegerField(
        help_text="Preparation time in minutes",
        default=15
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

    class Meta:
        ordering = ['-created_at']

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    customer = models.CharField(max_length=255) 
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    notess = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.customer}"
    
    def update_total(self):
        """Recalculate total_amount from OrderItems"""
        self.total_amount = sum(
            item.get_total_price() for item in self.order_items.all()
        )
        self.save()
    
    def save(self, *args, **kwargs):
        if self.status == 'completed':
            self._mark_products_unavailable()
        elif self.status in ['pending', 'canceled']:
            self._mark_products_available()
        super().save(*args, **kwargs)
    
    def _mark_products_unavailable(self):
        for item in self.order_items.all():
            item.product.is_available = False
            item.product.save()
    
    def _mark_products_available(self):
        for item in self.order_items.all():
            item.product.is_available = True
            item.product.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)  # PROTECT to preserve order history
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Order #{self.order.id})"
    
    def get_total_price(self):
        return self.product.price * self.quantity



from django.db import models
from django.conf import settings
user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username
