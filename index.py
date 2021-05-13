import time
import os
import requests
from pyrogram import Client
import random
import names
from pyrogram.errors.exceptions.bad_request_400 import PhoneCodeInvalid
from modules.SMSHUB import SMSHUBapi
from PIL import Image

sms_hub = SMSHUBapi("")
balance = sms_hub.get_balance()
print(f"Мой баланс: {balance}")
api_id = 3258867
api_hash = ""
app = Client("session", api_id, api_hash, proxy=dict(hostname="186.65.117.254", port=9623, username="CYqAsr", password="Hz46qW"))
app.connect()

# try:
if balance >= 5:
# Заказываем номер
#    country_code = random.choice([6, 2, 0, 10, 11])
   country_code = random.choice([6])
   phone_id, phone_num = sms_hub.get_number(service='tg', operator='any', country=country_code)
   print(f"Получили номер: {phone_num}")
   c = app.send_code(phone_num)
   sms_hub.set_status(phone_id, 1)
   code = sms_hub.get_code(phone_id, max_wait=60)
   print(f"Получили код: {code[1]}")
   print(phone_num, code[1])
first_name_for_reg = names.get_first_name(gender='female')
last_name_for_reg = names.get_last_name()
print(first_name_for_reg, last_name_for_reg)
code_hash = c['phone_code_hash']
print(code_hash)
if code[0] == 'STATUS_OK':
   sign_up = app.sign_up(phone_num, code_hash, first_name_for_reg, last_name_for_reg)
   print(sign_up)
except PhoneCodeInvalid as code_invalid:
if code_invalid:
   time.sleep(180)
   sms_hub.set_status(phone_id, 3)
   code = sms_hub.get_code(phone_id, max_wait=60)
   c = app.resend_code(phone_num, code_hash)
   print(c)
   time.sleep(60)
   sms_hub.set_status(phone_id, 3)
   time.sleep(30)
   code = sms_hub.get_code(phone_id, max_wait=60)
   print(code)
   code_hash = c['phone_code_hash']
   print(code_hash)
   if code[0] == 'STATUS_OK':
      app.sign_up(phone_num, code_hash, first_name_for_reg, last_name_for_reg)
      # Generate photo
      path = r""
      random_filename = random.choice([
         x for x in os.listdir(path)
         if os.path.isfile(os.path.join(path, x))
      ])
      thread = random.randint(1, 10000)
      image = Image.open(f"{random_filename}")
      image.thumbnail((250, 250))
      image.save(f"{thread}.jpg")
      print(image)
      time.sleep(10)
      # Add Photo
      app.set_profile_photo(photo=f"{thread}.jpg")
      time.sleep(15)
      # Add bio
      get_bio = requests.get("http://www.twitterbiogenerator.com/generate")
      bio = get_bio.text
      app.update_profile(bio=bio)
      # Clean photo
      os.remove(f"{thread}.jpg")


# Выводим его на экран
print(sms_hub.set_status(id, status=6))
