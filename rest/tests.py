from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Category, Order, OrderItem, Product,User

class CategoryAPITestCase(APITestCase):
    
    def setUp(self):
        self.category_data = {
            "name": "Appetizers",
            "description": "Small dishes before the main course",
            "is_active": True
        }
        self.category = Category.objects.create(**self.category_data)
        self.list_url = reverse('category-list')  # from DefaultRouter
        self.detail_url = reverse('category-detail', kwargs={"pk": self.category.id})

    def test_list_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('results', response.data)


    def test_create_category(self):
        data = {
            "name": "Beverages",
            "description": "Drinks and juices",
            "is_active": True
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_retrieve_category(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)

    def test_update_category(self):
        updated_data = {
            "name": "Updated Appetizers",
            "description": "Updated description",
            "is_active": False
        }
        response = self.client.put(self.detail_url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Appetizers")

    def test_delete_category(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.id).exists())


    def test_unauthorized_user_cannot_create_category(self):
        self.client.logout()
        response = self.client.post(self.list_url, self.category_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   

    def test_pagination_works(self):
      for i in range(7):
        Category.objects.create(name=f"Cat {i}", description="Test", is_active=True)
      response = self.client.get(self.list_url)
      self.assertEqual(len(response.data['results']), 5)




from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Customer

class CustomerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='pass', is_staff=True)
        self.client.login(username='admin', password='pass')

    def test_create_customer(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "123456789",
            "address": "123 street"
        }
        response = self.client.post("/customers/", data)
        self.assertEqual(response.status_code, 201)

    def test_update_customer(self):
        customer = Customer.objects.create(
            first_name="Jane", last_name="Doe", email="jane@example.com",
            phone="999", address="Somewhere"
        )
        response = self.client.put(f"/customers/{customer.id}/", {
            "first_name": "JaneUpdated", "last_name": "Doe", "email": "jane@example.com",
            "phone": "999", "address": "Updated Address"
        })
        self.assertEqual(response.status_code, 200)


class ProductAPITestCase(APITestCase):
    
    def setUp(self):
        # Create test users with different roles
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass',
            role='admin'
        )
        self.manager = User.objects.create_user(
            username='manager',
            password='managerpass',
            role='manager'
        )
        self.staff = User.objects.create_user(
            username='staff',
            password='staffpass',
            role='staff'
        )
        
        # Create 3 test categories
        self.category1 = Category.objects.create(
            name="Beverages",
            description="Drinks and juices",
            is_active=True
        )
        self.category2 = Category.objects.create(
            name="Appetizers",
            description="Small dishes before main course",
            is_active=True
        )
        self.category3 = Category.objects.create(
            name="Desserts",
            description="Sweet treats",
            is_active=True
        )
        
        self.products = []
        
        # Beverages (5 products)
        beverages = [
            {"name": "Coffee", "price": 3.50, "prep_time": 5, "available": True},
            {"name": "Tea", "price": 2.50, "prep_time": 3, "available": True},
            {"name": "Orange Juice", "price": 4.00, "prep_time": 2, "available": True},
            {"name": "Smoothie", "price": 5.50, "prep_time": 7, "available": False},
            {"name": "Iced Coffee", "price": 4.50, "prep_time": 5, "available": True},
        ]
        
        # Appetizers (5 products)
        appetizers = [
            {"name": "Bruschetta", "price": 7.99, "prep_time": 10, "available": True},
            {"name": "Nachos", "price": 8.50, "prep_time": 12, "available": True},
            {"name": "Spring Rolls", "price": 6.99, "prep_time": 8, "available": False},
            {"name": "Garlic Bread", "price": 5.50, "prep_time": 7, "available": True},
            {"name": "Soup of the Day", "price": 6.25, "prep_time": 15, "available": True},
        ]
        
        # Desserts (5 products)
        desserts = [
            {"name": "Chocolate Cake", "price": 7.50, "prep_time": 5, "available": True},
            {"name": "Cheesecake", "price": 8.00, "prep_time": 5, "available": True},
            {"name": "Ice Cream", "price": 5.50, "prep_time": 2, "available": False},
            {"name": "Tiramisu", "price": 9.00, "prep_time": 10, "available": True},
            {"name": "Fruit Salad", "price": 6.50, "prep_time": 8, "available": True},
        ]
        
        # Create all products
        for item in beverages:
            self.products.append(Product.objects.create(
                name=item["name"],
                description=f"Delicious {item['name']}",
                price=item["price"],
                category=self.category1,
                is_available=item["available"],
                preparation_time=item["prep_time"]
            ))
            
        for item in appetizers:
            self.products.append(Product.objects.create(
                name=item["name"],
                description=f"Tasty {item['name']}",
                price=item["price"],
                category=self.category2,
                is_available=item["available"],
                preparation_time=item["prep_time"]
            ))
            
        for item in desserts:
            self.products.append(Product.objects.create(
                name=item["name"],
                description=f"Sweet {item['name']}",
                price=item["price"],
                category=self.category3,
                is_available=item["available"],
                preparation_time=item["prep_time"]
            ))
        
        self.coffee = self.products[0]  
        self.bruschetta = self.products[5]
        self.cake = self.products[10]  
        
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', args=[self.product1.id])
        self.available_url = reverse('product-available')
        self.menu_url = reverse('product-menu-by-category')
        self.check_avail_url = reverse('product-check-availability', args=[self.product1.id])
        
        # Order URLs
        self.order_list_url = reverse('order-list')
        self.order_item_url = reverse('orderitem-list')

    def test_list_products(self):
        """Test that any authenticated user can list products"""
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2) 

    def test_create_product_permissions(self):
        """Test that only admin/manager can create products"""
        # Staff should not be able to create
        self.client.force_authenticate(user=self.staff)
        data = {
            "name": "New Drink",
            "description": "New description",
            "price": 4.99,
            "category": self.category.id,
            "is_available": True,
            "preparation_time": 10
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin should be able to create
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)

    def test_update_product_permissions(self):
        """Test that only admin/manager can update products"""
        # Staff should not be able to update
        self.client.force_authenticate(user=self.staff)
        data = {"name": "Updated Coffee"}
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Manager should be able to update
        self.client.force_authenticate(user=self.manager)
        response = self.client.patch(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, "Updated Coffee")

    def test_delete_product_permissions(self):
        """Test that only admin/manager can delete products"""
        # Staff should not be able to delete
        self.client.force_authenticate(user=self.staff)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin should be able to delete
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1) 

    def test_available_products_endpoint(self):
        """Test the /products/available/ endpoint"""
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.available_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 
        self.assertEqual(response.data['results'][0]['name'], "Coffee")

    def test_menu_by_category_endpoint(self):
        """Test the /products/menu-by-category/ endpoint"""
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.menu_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
        self.assertEqual(response.data[0]['category_name'], "Beverages")
        self.assertEqual(len(response.data[0]['products']), 1)  

    def test_check_availability_endpoint(self):
        """Test the check availability endpoint"""
        self.client.force_authenticate(user=self.staff)
        
        # Test available product
        response = self.client.get(self.check_availability_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_available'])
        self.assertEqual(response.data['message'], 'Available for order')
        
        # Test unavailable product
        unavailable_url = reverse('product-check-availability', kwargs={"pk": self.product2.id})
        response = self.client.get(unavailable_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_available'])
        self.assertEqual(response.data['message'], 'Currently unavailable')

    def test_price_filters(self):
        # Create test products
        Product.objects.create(name="Cheap", price=5.00, is_available=True)
        Product.objects.create(name="Mid-range", price=10.00, is_available=True)
        Product.objects.create(name="Expensive", price=20.00, is_available=True)

        # Test less than
        response = self.client.get(reverse('product-list'), {'price_lt': 15})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Cheap and Mid-range

        # Test greater than
        response = self.client.get(reverse('product-list'), {'price_gt': 8})
        self.assertEqual(len(response.data['results']), 2)  # Mid-range and Expensive

        # Test range
        response = self.client.get(reverse('product-list'), {'price_gt': 5, 'price_lt': 15})
        self.assertEqual(len(response.data['results']), 1)
    def test_product_ordering(self):
        """Test that products are ordered by creation date"""
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Newest first (tea was created after coffee in setUp)
        self.assertEqual(response.data['results'][0]['name'], "Tea")
        self.assertEqual(response.data['results'][1]['name'], "Coffee")  

    def test_order_completion_updates_availability(self):
        """Products should become unavailable when order is completed"""
        self.client.force_authenticate(user=self.staff)
        
        # Create order
        order_data = {
            'customer': 'Test Customer',
            'status': 'pending',
            'order_items': [
                {
                    'product': self.product1.id,
                    'quantity': 2
                }
            ]
        }
        
        # Create order (simplified - in reality you'd need nested serializer)
        order = Order.objects.create(
            customer=order_data['customer'],
            status=order_data['status']
        )
        OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=order_data['order_items'][0]['quantity']
        )
        
        self.assertTrue(Product.objects.get(id=self.product1.id).is_available)
        
        order.status = 'completed'
        order.save()
        
        self.assertFalse(Product.objects.get(id=self.product1.id).is_available)
        
        order.status = 'canceled'
        order.save()
        
        self.assertTrue(Product.objects.get(id=self.product1.id).is_available)
   