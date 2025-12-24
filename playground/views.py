from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage


def product(request):
    try:
        message = BaseEmailMessage(
            template_name='emails/hell0.html',
            context={'name': 'Naveen Sahu'}
        )
        message.send(to=['naveensahu18@gmail.com'])
    except BadHeaderError:
        pass
    return HttpResponse('Invalid header found.')

# Create your views here.
# def product(request):
#     try:
#         send_mail(
#         'subject from django',
#         'Hello there. This is a test email sent from a Django application.',
#         'codersahu18@gmail.com',
#         ['naveensahu18@gmail.com'],
#         fail_silently=False,
#         )
#     except BadHeaderError:
#         pass
#     return HttpResponse('Invalid header found.')

# def product(request):
#     try:
#         message = EmailMessage(
#             'subject from django',
#         'Hello there. This is a test email sent from a Django application.',
#         'codersahu18@gmail.com',
#         ['naveensahu18@gmail.com'],
#         )
#         message.attach_file('playground/static/images/Screenshot.png')
#         message.send()

#     except BadHeaderError:
#         pass
#     return HttpResponse('Invalid header found.')

# def product(request):
    # query_set = Product.objects.all()

    # for product in query_set:
    #     print(product)

    # queryset = Order.objects.prefetch_related('orderitem_set__product').select_related('customer').order_by('-placed_at')[:10]
    # Based on that queryset, django-debug-toolbar should show **3 queries**:

    # 1. **Main query**: Fetches Order objects with `customer` joined via `select_related()`
    # 2. **First prefetch query**: Fetches all related `OrderItem` objects for the 5 orders
    # 3. **Second prefetch query**: Fetches all related `Product` objects for those OrderItems

    # The `prefetch_related()` with the double underscore (`orderitem_set__product`) splits into 2 separate queries for performance, while `select_related('customer')` uses a database JOIN in the main query.

    # for order in queryset:
    #     for item in order.orderitem_set.all():
    #         print(item.product) 


    # Querying the generic relations steps -->

    # 1. Get the ContentType for the Product model.
    # 2. Use that ContentType to filter TaggedItem objects where the content_type matches and object_id is the ID of the specific Product.
    # 3. This will give you all tags associated with that specific Product.
    # 4. Finally, render the results in the template. 
     
    # content_type = ContentType.objects.get_for_model(Product)
    # queryset = TaggedItem.objects.select_related('tag').filter(
    #     content_type=content_type,
    #     object_id = 1
    # )

    # custom manager approach
    # steps -->
    # 1. Define a custom manager method `get_tags_for` in the `TaggedItem` model that takes a model class and an object ID as parameters.
    # 2. Inside this method, retrieve the `ContentType` for the given model class.
    # 3. Use this `ContentType` to filter `TaggedItem` objects where the `content_type` matches and `object_id` is the provided ID.     
    # 4. This method returns all tags associated with the specified object.
    
    # queryset = TaggedItem.objects.get_tags_for(Product, 1)


    # return render(request, 'index.html', {'tags': list(queryset)})


