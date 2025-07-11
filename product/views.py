from itertools import product

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from unicodedata import category

from .models import Product, Category, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductDetailSerializer
from .serializers import ProductWithReviewsSerializer, CategoryWithCountSerialzier
from django.db.models import Count

@api_view(['GET'])
def category_list_api_view(request):
    category = Category.objects.all()

    data = CategorySerializer(instance=category, many=True).data

    return Response(
        data=data,
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': f'Category with id = {str(id)} does not exist!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = CategorySerializer(category).data
    return Response(data=data)

@api_view(http_method_names=['GET'])
def product_list_api_view(request):
    products = Product.objects.all()

    data = ProductSerializer(instance=products, many=True).data

    return Response(
        data=data,
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        products = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': f'Product with id = {str(id)} does not exist!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ProductDetailSerializer(products).data
    return Response(data=data)


@api_view(['GET'])
def review_list_api_view(request):
    review = Review.objects.all()

    data = ReviewSerializer(review, many=True).data
    return Response(
        data=data,
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.object.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': f'Review with id = {str(id)} does not exist!'},
                        status=status.HTTP_404_NOT_FOUND)
    data = ReviewSerializer(review).data
    return Response(data=data)

@api_view(['GET'])
def product_review_list_api_view(request):
    product = Product.objects.all()

    data = ProductWithReviewsSerializer(instance=product, many=True).data

    return Response(
        data=data,
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def category_count_list_api_view(request):
    category = Category.objects.annotate(products_count=Count('products'))

    data = CategoryWithCountSerialzier(instance=category, many=True).data


    return Response(
        data=data,
        status=status.HTTP_200_OK
    )