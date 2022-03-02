import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])


def send(phone):
    verify.verifications.create(to=str(phone), channel='sms')


def check(phone, code):
    try:
        print(phone, code)
        result = verify.verification_checks.create(to=str(phone), code=str(code))
        print(result)
    except TwilioRestException:
        print('no')
        result.status = "canceled"
        return False
    return result.status == 'approved'
# def check(phone, code):
#     try:
#         print(phone, code)
#         result = verify.verification_checks.create(to=str(phone), code=str(code))
#         print(result)
#     except TwilioRestException:
#         print('no')
#         return False
#     return result.status == 'approved'
