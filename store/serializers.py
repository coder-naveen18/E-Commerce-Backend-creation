from rest_framework import serializers
from store.models import Product, Collection, Review
from decimal import Decimal

# Product Serializer with price_with_tax field
class ProductSerializer(serializers.ModelSerializer):
    # assuming a tax rate of 20%
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax') 

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'inventory', 'collection', 'price_with_tax']

    def calculate_price_with_tax(self, product: Product):
        return product.price * Decimal(1.2)
    
# Collection Serializer with products_count field
class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField(method_name='get_products_count')
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    def get_products_count(self, collection: Collection):
        return collection.products.count()
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)