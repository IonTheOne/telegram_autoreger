import time
import os
import requests
import random
import names
from modules.SMSHUB import SMSHUBapi
from PIL import Image
from telethon import TelegramClient

sms_hub = SMSHUBapi("75815U81aac3d0f4ed59a18a27dbf683322528")
balance = sms_hub.get_balance()
print(f"Мой баланс: {balance}")
api_id = 3258867
api_hash = "38125a46bf0d4ba7777d0b7e36fa2818"
proxy = {
    'proxy_type': 'socks5',
    'addr': '186.65.117.254',
    'port': 9623,
    'username': 'CYqAsr',
    'password': 'Hz46qW',
    'rdns': True
}
client = TelegramClient('anon', api_id, api_hash, proxy=proxy)
client.start()
async def main():

    country_code = random.choice([0])
    phone_id, phone_num = sms_hub.get_number(service='tg', operator='any', country=country_code)
    print(f"Получили номер: {phone_num}")
    await client.send_code_request(phone_num)
    sms_hub.set_status(phone_id, 1)
    code = sms_hub.get_code(phone_id, max_wait=60)
    print(f"Получили код: {code[1]}")
    print(phone_num, code[1])
    first_name_for_reg = names.get_first_name(gender='female')
    last_name_for_reg = names.get_last_name()
    print(first_name_for_reg, last_name_for_reg)
    await client.sign_up(code, first_name=first_name_for_reg, last_name=last_name_for_reg)

with client:
    client.loop.run_until_complete(main())