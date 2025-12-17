from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register('products', views.ProductViewSet, basename='product')
router.register('collections', views.CollectionViewSet, basename='collection')

urlpatterns = [
    path('', include(router.urls)),
    # path('products/', views.product_list), ---> when we use the function based views
    # path('products/', views.ProductList.as_view()),  # ---> when we use the class based views
    # # path('products/<int:id>/', views.product_detail), ---> when we use the function based views
    # path('products/<int:id>/', views.ProductDetail.as_view()),  # ---> when we use the class based views
    # # path('collections/', views.collection_list), # --> when we use the function based views
    # path('collections/', views.CollectionList.as_view()), # --> when we use the generic views
    # path('collections/<int:pk>/', views.collection_detail, name='collection-detail'),  # --> when we use the function based views
    # path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),  # --> when we use the generic views
]
