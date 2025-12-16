from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from .models import OrderItem, Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


# using the Generic Class Based Views to simplify our code

# class ProductList(ListCreateAPIView):
#     def get_queryset(self):
#         return Product.objects.select_related('collection').all()
    
#     def get_serializer_class(self):
#         return ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request': self.request}


# creating the class based views
# for the product list endpoint ---> store/products/
# class ProductList(APIView):
#     def get(self, request):
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# Create your function based views here.

# @api_view(['GET', 'POST'])
# def product_list(request):
#     if request.method == 'GET':
#         queryset = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         #  deserializing object
#         serializer = ProductSerializer(data=request.data)
#         # Validating data
#         serializer.is_valid(raise_exception=True)
#         print(serializer.validated_data)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        


# product detail endpoint ---> store/products/<id>/

# creating the class based views
# class ProductDetail(APIView):   
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # serializer.validated_data
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK) 

#     def patch(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         # serializer.validated_data
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         # check if product is associated with any order item
#         if product.orderitems.count() > 0:
#             return Response(
#                 {'error': 'Product cannot be deleted because it is associated with an order item.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
# using the generic class based views to simplify our code

# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'

#     def get_serializer_context(self):
#         return {'request': self.request}
    
    # def delete(self, request, id): # changing the delete method to add custom behavior and changing pk to id
    #     product = get_object_or_404(Product, pk=id)
    #     # check if product is associated with any order item
    #     if product.orderitems.count() > 0:
    #         return Response(
    #             {'error': 'Product cannot be deleted because it is associated with an order item.'},
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED
    #         )
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    

# Combining Product and ProductDetail class based views using the ModelViewSet for removing redundancy

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        # product = get_object_or_404(Product, pk=id) # here we are making the DB call to get the product instance
        if OrderItem.objects.filter(product_id=kwargs['id']).count() > 0:
            return Response(
                    {'error': 'Product cannot be deleted because it is associated with an order item.'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)

    

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def product_detail(request, id):
#         if request.method == 'GET':
#             product = get_object_or_404(Product, pk=id)
#             serializer = ProductSerializer(product, context={'request': request})
#             return Response(serializer.data)
#         elif request.method == 'PUT':
#             product = get_object_or_404(Product, pk=id)
#             serializer = ProductSerializer(product, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             # serializer.validated_data
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK) 
#         elif request.method == 'PATCH':
#             product = get_object_or_404(Product, pk=id)
#             serializer = ProductSerializer(product, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             # serializer.validated_data
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         elif request.method == 'DELETE':            
#             product = get_object_or_404(Product, pk=id)
#             # check if product is associated with any order item
#             if product.orderitems.count() > 0:
#                 return Response(
#                     {'error': 'Product cannot be deleted because it is associated with an order item.'},
#                     status=status.HTTP_405_METHOD_NOT_ALLOWED
#                 )
#             product.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
    
# creating the generic class based views -->
# collection list endpoint ---> store/collections/

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}

# @api_view(['GET', 'POST'])
# def collection_list(request):
#     if request.method == 'GET':
#         queryset = Collection.objects.all()
#         serializer = CollectionSerializer(queryset, many=True, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# collection detail endpoint ---> store/collections/<pk>/
# creating the class based views using the generic class based views

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer 

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it includes one or more products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# # function based views for collection detail endpoint
# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request, pk):
#     if request.method == 'GET':
#         collection = get_object_or_404(Collection, pk=pk)
#         serializer = CollectionSerializer(collection, context={'request': request})
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         collection = get_object_or_404(Collection, pk=pk)
#         serializer = CollectionSerializer(collection, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         collection = get_object_or_404(Collection, pk=pk)
#         if collection.products.count() > 0:
#             return Response(
#                 {'error': 'Collection cannot be deleted because it includes one or more products.'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED
#             )
#         collection.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)