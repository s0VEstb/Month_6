from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ProductDetailSerializer
from .serializers import ProductWithReviewsSerializer, CategoryWithCountSerialzier
from django.db.models import Count

@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
       category = Category.objects.all()

       data = CategorySerializer(instance=category, many=True).data

       return Response(
         data=data,
         status=status.HTTP_200_OK
       )
    if request.method == 'POST':
        name = request.data.get('name')

        category = Category.objects.create(
            name=name
        )
        category.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=CategorySerializer(category).data)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': f'Category with id = {str(id)} does not exist!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
      data = CategorySerializer(category).data
      return Response(data=data)
    elif request.method == 'PUT':
       category.name = request.data.get('name')
       category.save()
       return Response(status=status.HTTP_201_CREATED,
                       data=CategorySerializer(category).data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
       product = Product.objects.all()

       data = ProductSerializer(instance=product, many=True).data

       return Response(
        data=data,
        status=status.HTTP_200_OK
       )
    if request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category = request.data.get('category')

        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category_id=category
        )
        product.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ProductSerializer(product).data)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': f'Product with id = {str(id)} does not exist!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
       data = ProductDetailSerializer(product).data
       return Response(data=data)
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category')
        product.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ProductDetailSerializer(product).data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':

        review = Review.objects.all()

        data = ReviewSerializer(review, many=True).data
        return Response(
        data=data,
        status=status.HTTP_200_OK
        )
    if request.method == 'POST':
        text = request.data.get('text')
        product = request.data.get('product')
        stars = request.data.get('stars')

        review = Review.objects.create(
            text=text,
            product_id=product,
            stars=stars
        )
        review.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': f'Review with id = {str(id)} does not exist!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
         data = ReviewSerializer(review).data
         return Response(data=data)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.product = request.data.get('product')
        review.stars = request.data.get('stars')
        review.save()

        return Response(status=status.HTTP_201_CREATED,
                        data=ReviewSerializer(review).data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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