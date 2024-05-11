from django.contrib.sites.models import Site
from django.conf import settings
import requests
from .bank import BaseBank


class AqayePardakhtSandbox(BaseBank):
    PIN = settings.AQAYEPARDAKHT_PIN
    CALLBACK_URL = f"http://{Site.objects.get_current().domain}/payment/verify/aq/"
    AQ_API_REQUEST = "https://panel.aqayepardakht.ir/api/v2/create"
    AQ_API_VERIFY = "https://panel.aqayepardakht.ir/api/v2/verify"
    AQ_API_STARTPAY = "https://panel.aqayepardakht.ir/startpay/sandbox/"

    def send_request(self, amount, description="پرداخت"):
        response = requests.post(
            url=self.AQ_API_REQUEST,
            json={
                'pin': self.PIN,
                'amount': int(amount),
                'callback': self.CALLBACK_URL,
                'description': description,
            }
        )
        return response.json()

    def verify_payment(self, authority, amount):
        response = requests.post(
            url=self.AQ_API_VERIFY,
            json={
                "pin": self.PIN,
                "transid": authority,
                "amount": int(amount),
            }
        )
        return response.json()

    def generate_payment_url(self, authority):
        return self.AQ_API_STARTPAY + authority
