from django.contrib import admin
from .models import Tag

# Register your models here.
# admin.site.register(Tag)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
#     autocomplete_fields = ['tag']
#     list_display = ['tag', 'content_type', 'object_id']
    search_fields = ['label']
