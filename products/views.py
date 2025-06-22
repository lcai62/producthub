from django.shortcuts import render
from rest_framework import generics

from products.models import Product, Category, Tag
from products.pagination import ProductPagination
from products.serializers import ProductSerializer, CategorySerializer, TagSerializer


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        description_filter = self.request.query_params.get("description")
        category = self.request.query_params.get("category")
        tags_list = self.request.query_params.get("tags")

        print(f"description_filter {description_filter}")
        print(f"category_filter  {category}")
        print(f"tags_filter  {tags_list}")

        if description_filter:
            queryset = queryset.filter(description__icontains=description_filter)
        if category:
            queryset = queryset.filter(category__name__iexact=category)
        if tags_list:
            tags = [tag.strip() for tag in tags_list.split(",") if tag.strip()]
            for tag in tags:
                queryset = queryset.filter(tags__name__iexact=tag)

        return queryset


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
