from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Custom manager to handle tag retrieval
class TaggedItemManager(models.Manager):
    def get_tags_for(self, model, object_id):
        content_type = ContentType.objects.get_for_model(model)
        return TaggedItem.objects.select_related('tag').filter(
            content_type=content_type,
            object_id=object_id
        )

# Create your models here.
class Tag(models.Model):
    label = models.CharField(max_length=255)

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    # what tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    # because we want to make our applications independent of each other .
    # So we are not importing the models form the other app
    # we will use generic relation to find the object and type of that
    # Type
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # ID 
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
