from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Category, Tag, Product


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.books = Category.objects.create(name="Books")
        self.electronics = Category.objects.create(name="Electronics")

        self.tag_popular = Tag.objects.create(name="Popular")
        self.tag_discount = Tag.objects.create(name="Discount")

        self.product1 = Product.objects.create(
            name="Science Book",
            description="a grade 10 science book.",
            category=self.books,
            price="10.00",
            stock=10
        )
        self.product1.tags.add(self.tag_popular)

        self.product2 = Product.objects.create(
            name="Physics Book",
            description="a physics book for smart kids",
            category=self.books,
            price="12.00",
            stock=12
        )
        self.product2.tags.add(self.tag_popular, self.tag_discount)

        self.product3 = Product.objects.create(
            name="Smartphone",
            description="with new ai assistant",
            category=self.electronics,
            price="500.00",
            stock=500
        )

    def test_list_products(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_filter_by_category(self):
        response = self.client.get("/api/products/?category=books")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_by_tags(self):
        response = self.client.get("/api/products/?tags=popular,discount")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_names = [p["name"] for p in response.data["results"]]
        self.assertIn("Physics Book", product_names)
        self.assertNotIn("Science Book", product_names)  # Only has one tag

    def test_search_by_description(self):
        response = self.client.get("/api/products/?description=physics")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Physics Book")

    def test_filter_and_search_combined(self):
        response = self.client.get("/api/products/?category=books&description=smart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Physics Book")

    def test_filter_by_category_and_tags(self):
        response = self.client.get("/api/products/?tags=popular,discount")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Physics Book")

    def test_pagination(self):
        for i in range(15):
            p = Product.objects.create(
                name=f"Product {i}",
                description="description dummy",
                category=self.books,
                price="5.00",
                stock=5
            )
            p.tags.add(self.tag_discount)

        response = self.client.get("/api/products/")

        # 18 total, page count 12
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 18)
        self.assertEqual(len(response.data["results"]), 12)
        self.assertIsNotNone(response.data["next"])
