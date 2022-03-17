from paypal.standard.ipn.signals import valid_ipn_received , invalid_ipn_received
from django.dispatch  import receiver 


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'complete':
        print('valid')
        

@receiver(invalid_ipn_received)
def paypal_payment_notReceived(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == 'complete':
        print('invalid')
   