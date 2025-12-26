from time import sleep
from celery import shared_task


@shared_task
def notifiy_customer(message):
    print("Notifying customer:", message)
    sleep(5)
    print("Customer notified.")
