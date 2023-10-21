from fast_bitrix24 import Bitrix
import os


class BitrixRequest:
    """Класс-обертка для подключения к crm bitrix24"""

    def __init__(self):
        crm_adress = os.getenv('CRM_URL')
        admin_id = os.getenv('ADMINISTRATOR_ID')
        token = os.getenv('TOKEN')
        webhook = f"https://{crm_adress}/rest/{admin_id}/{token}/"

        self.crm_adress = crm_adress
        self.connect = Bitrix(webhook)