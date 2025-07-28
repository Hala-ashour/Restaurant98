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
    # products = models.ManyToManyField('Product', related_name='orders')
    # customer = models.ForeignKey('customer')



    def __str__(self):
        return self.customer
    



# class OrderItem(models.Model):
#     order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return self.order
    


#     # لحساب total amount
#     def get_total_price(self):
#         return self.product.price * self.quantity     




from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username
