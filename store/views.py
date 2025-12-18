from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from store.pagination import DefaultPagination

from .models import OrderItem, Product, Collection, Review
from store.filters import ProductFilter
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer



# Combining Product and ProductDetail class based views using the ModelViewSet for removing redundancy
# product list endpoint ---> store/products/
# product detail endpoint ---> store/products/{id}/
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
# applying filtering with django-filter 
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['collection_id', 'price']
    filterset_class = ProductFilter # custom filter class
    search_fields = ['title', 'description']  # for search functionality
    ordering_fields = ['title', 'price']  # for ordering functionality
    pagination_class = DefaultPagination    


    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        # product = get_object_or_404(Product, pk=id) # here we are making the DB call to get the product instance
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                    {'error': 'Product cannot be deleted because it is associated with an order item.'},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)

    

# Combining the CollectionList and CollectionDetail class based views
# collection list endpoint ---> store/collections/
# collection detail endpoint ---> store/collections/{pk}/
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        # collection = get_object_or_404(Collection, pk=pk)
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Collection cannot be deleted because it includes one or more products.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
# solving the nested routing issue by overriding the get_queryset method
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
