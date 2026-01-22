import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

admin.site.site_header = "Ecommerce Admin"
admin.site.site_title = "Ecommerce Admin Portal"
admin.site.index_title = "Welcome to Ecommerce Admin Portal"

urlpatterns = [
    path('core/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('tags/', include('tags.urls')),
    path('likes/', include('likes.urls')),
    path('playground/', include('playground.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('__debug__/', include(debug_toolbar.urls)),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
