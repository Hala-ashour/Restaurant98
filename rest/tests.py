from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Category,User

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

