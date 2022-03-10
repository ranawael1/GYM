import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])
check_phone = 0

def send(phone):
    print('mm')
    verify.verifications.create(to=str(phone), channel='sms')
    print(phone)
def check(phone, code):
    try:
        print(phone, code)
        result = verify.verification_checks.create(to=str(phone), code=str(code))
        print(result)
    except TwilioRestException:
        print('no')
        #result.status = "canceled"
        return False
    return result.status == 'approved'
def resend(phone):
    try:
        print(phone)
        result = verify.verification_checks.create(to=str(phone), code=str('000000')) 
       
    except TwilioRestException:
        send(phone)

# def check(phone, code):
#     try:
#         print(phone, code)
#         result = verify.verification_checks.create(to=str(phone), code=str(code))
#         print(result)
#     except TwilioRestException:
#         print('no')
#         return False
#     return result.status == 'approved'
