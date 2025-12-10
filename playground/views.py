from django.shortcuts import render
from store.models import Product

# Create your views here.

def product(req):
    query_set = Product.objects.all()

    for product in query_set:
        print(product)

    return render(req, 'index.html')
