from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        #  deserializing object
        serializer = ProductSerializer(data=request.data)
        # Validating data
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
            

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, id):
        if request.method == 'GET':
            product = get_object_or_404(Product, pk=id)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'PUT':
            product = get_object_or_404(Product, pk=id)
            serializer = ProductSerializer(product, data=request.data)
            serializer.is_valid(raise_exception=True)
            # serializer.validated_data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        elif request.method == 'PATCH':
            product = get_object_or_404(Product, pk=id)
            serializer = ProductSerializer(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            # serializer.validated_data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':            
            product = get_object_or_404(Product, pk=id)
            # check if product is associated with any order item
            if product.orderitems.count() > 0:
                return Response(
                    {'error': 'Product cannot be deleted because it is associated with an order item.'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    if request.method == 'GET':
        collection = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(collection, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        collection = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it includes one or more products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)