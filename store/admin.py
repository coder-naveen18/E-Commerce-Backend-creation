from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory','inventory_status', 'last_update','collection_title']
    list_editable = ['price', 'inventory']
    search_fields = ['title__istartswith']
    list_per_page = 10
    list_select_related = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 100:
            return "Low"
        return "OK"
    
    def collection_title(self, product):
        return product.collection.title
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership','orders_count']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_editable = ['membership']
    list_per_page = 10

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist')
                + '?'
                + urlencode({
                    'customer__id': str(customer.id)
                    }))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment_status', 'placed_at', 'customer']
    list_select_related = ['customer']
    list_per_page = 10


# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title__istartswith']
    list_per_page = 10

    @admin.display(ordering='products_count')   
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
                    'collection__id': str(collection.id)
                    }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        
    
    def  get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

