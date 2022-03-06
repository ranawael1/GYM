import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])
check_phone = 0

def send(phone):
    if phone.startswith('+2'):
        pass
    else:
        phone = '+2'+phone
    print(phone)
    verify.verifications.create(to=str(phone), channel='sms')
    check_phone = phone


def check(phone, code):
    try:
        print(phone, code)
        if phone.startswith('+2'):
            pass
        else:
            phone = '+2'+phone
        print(phone)
        result = verify.verification_checks.create(to=str(phone), code=str(code))
        print(result)
    except TwilioRestException:
        print('no')
        #result.status = "canceled"
        return False
    return result.status == 'approved'
def cancellation():
    try:
        print(check_phone)
        result = verify.verification_checks.create(to=str(check_phone), code=str('000000'))
        result.status = "canceled"
    except:
        pass

# def check(phone, code):
#     try:
#         print(phone, code)
#         result = verify.verification_checks.create(to=str(phone), code=str(code))
#         print(result)
#     except TwilioRestException:
#         print('no')
#         return False
#     return result.status == 'approved'
