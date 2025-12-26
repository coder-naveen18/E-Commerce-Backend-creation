from django.http import HttpResponse
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage



from .tasks import notifiy_customer

def product(request):
    notifiy_customer.delay("Your product has been shipped!")
    return HttpResponse('Task to notify customer has been initiated.')


#  sending email using templated_mail package
# def product(request):
#     try:
#         message = BaseEmailMessage(
#             template_name='emails/hello.html',
#             context={'name': 'Naveen Sahu'}
#         )
#         message.send(to=['naveensahu18@gmail.com'])
#     except BadHeaderError:
#         pass
#     return HttpResponse('Invalid header found.')


