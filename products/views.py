from django.shortcuts import render
from rest_framework import generics

from products.models import Product
from products.serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        description_filter = self.request.query_params.get("description")
        category_slug = self.request.query_params.get("category__slug")
        tags_slugs = self.request.query_params.get("tags__slug")

        print(f"description_filter {description_filter}")
        print(f"category_filter  {category_slug}")
        print(f"tags_filter  {tags_slugs}")

        if description_filter:
            queryset = queryset.filter(description__icontains=description_filter)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if tags_slugs:
            tag_slugs = [tag.strip() for tag in tags_slugs.split(",") if tag.strip()]
            for slug in tag_slugs:
                queryset = queryset.filter(tags__slug=slug)

        return queryset
