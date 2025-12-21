from decimal import Decimal
from django.db import  transaction
from rest_framework import serializers
from store.models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem
from store.signals import order_created

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
    
class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart_item : CartItem):
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']
        

class CartSerializer(serializers.ModelSerializer):
    id  = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many = True, read_only = True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.price for item in cart.items.all() ])
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with given id was found')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            # updating the existing item
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # creating the new item
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

    

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','user_id', 'phone','birth_date', 'membership']


class OrderItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id','product','unit_price','quantity']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart wiht given id found')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The Cart is empty')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            # print(self.validated_data['cart_id'])
            # print(self.context['user_id'])
            cart_id =  self.validated_data['cart_id']

            customer = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)

            cart_items = CartItem.objects.select_related('product').filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product = item.product,
                    price = item.product.price,
                    quantity = item.quantity
                ) for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()
            order_created.send_robust(self.__class__, order=order)
            return order