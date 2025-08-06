from django.contrib import admin
from .models import Category, Product,Order,OrderItem

admin.site.register(Category)
# admin.site.register(OrderItem)
admin.site.register(Order)

from .models import Customer

admin.site.register(Customer)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'is_available')

