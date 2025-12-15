from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Promotion
class Promotion(models.Model):
    description = models.TextField()
    discount = models.FloatField()

# Collection
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name="+")
    # here we are having a issue --> Reverse queryname for the 'store.collection.featured_product' clashed with field name 'store.product.collection' -----> to solve that either we can add related_name to something or if we don;t want to take load we make related_name ="+".
    # Now after using the '+' , django will not Create the reverse relation 

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']


# Product
class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)

    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']    
    

class Customer(models.Model):
    class typeChoice(models.TextChoices):
        GOLD = 'G', 'Gold'
        SILVER = 'S', 'Silver'
        BRONZE = 'B', 'Bronze'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(blank=True, null=True)
    birth_date = models.DateField()

    membership = models.CharField(max_length=1, choices=typeChoice.choices, default=typeChoice.SILVER)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['first_name', 'last_name']
    


class Order(models.Model):
    class typeChoice(models.TextChoices):
        PENDING = 'P', 'Pending'
        CONFIRM = 'C', 'Confirm'
        FAILED = 'F', 'Failed'

    payment_status = models.CharField(max_length=1, choices=typeChoice.choices, default=typeChoice.PENDING)
    placed_at = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    def __str__(self):
        return self.payment_status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Address(models.Model):
    zip_code = models.PositiveSmallIntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True) # implemented the one-to-one relation between the Customer and the Address models

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()