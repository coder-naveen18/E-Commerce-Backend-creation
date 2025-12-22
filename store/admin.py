from django.contrib import admin, messages
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']

    def thumbnail(self, instance):
        if instance.image.name != "":
            return format_html('<img src="{}" style="width: 50px; height:auto;">', instance.image.url)
        return ""
    

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'description': ['title'],
    }
    fields = ['title', 'description', 'price', 'inventory', 'collection', 'promotions']
    actions = ['clear_inventory']
    inlines = [ProductImageInline]
    list_display = ['title', 'price', 'inventory','inventory_status', 'last_update','collection_title']
    list_editable = ['price', 'inventory']
    list_filter = ['collection', 'last_update']
    list_per_page = 10
    list_select_related = ['collection']
    search_fields = ['title__istartswith']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 100:
            return "Low"
        return "OK"
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated.",
            messages.SUCCESS
        )
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership','orders_count']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    autocomplete_fields = ['user']

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

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    autocomplete_fields = ['customer']
    list_display = ['id', 'payment_status', 'placed_at', 'customer']
    list_select_related = ['customer']
    list_per_page = 10


# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    list_per_page = 10
    search_fields = ['title__istartswith']

    @admin.display(ordering='products_count')   
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
                    'collection__id': str(collection.id)
                    }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
        
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

