from rest_framework import serializers
from store.models import Product, Collection
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_product']

class ProductSerializer(serializers.Serializer):
    # assuming a tax rate of 20%
    def calculate_price_with_tax(self, product):
        return product.price * Decimal(1.2)  

    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    description = serializers.CharField()

    # additional custom field
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_price_with_tax') 

    # serializing related field
    # collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())

    # String representation of the related field
    collection = serializers.StringRelatedField()

    # alternative way to serialize related field as nested object
    # collection = CollectionSerializer()

    # alternative way to serialize related field as hyperlink
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )