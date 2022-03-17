from paypal.standard.ipn.signals import valid_ipn_received , invalid_ipn_received
from django.dispatch  import receiver 
from .models import PaymentCheckOut

@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'complete':
        print('valid')
        PaymentCheckOut.objects.create()

@receiver(invalid_ipn_received)
def paypal_payment_notReceived(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'complete':
        print('invalid')
        PaymentCheckOut.objects.create()