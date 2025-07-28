from django.contrib import admin
from .models import Category

admin.site.register(Category)

from .models import Customer

admin.site.register(Customer)
