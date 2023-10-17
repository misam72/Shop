from kavenegar import *


def send_otp_code(phone_number, code):
     print(phone_number, code)
     # try:
     #      api = KavenegarAPI('73694E324F64743277507547617A6B2F37754D4E4F495646724A456D307239445541425A443567696C78383D') 
     #      params = {'sender' : '', 
     #                'receptor': phone_number, # recivers contancts.
     #                'message' :f'کد شما: {code}' } 
     #      response = api.sms_send(params) 
     #      print(response)
     # except APIException as e:
     #      print(f'{e}')
     # except HTTPException as e:
     #      print(e)
     # except Exception as e:
     #      print(e)