from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import OrderItem, Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


# Combining Product and ProductDetail class based views using the ModelViewSet for removing redundancy
# product list endpoint ---> store/products/
# product detail endpoint ---> store/products/{id}/
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

