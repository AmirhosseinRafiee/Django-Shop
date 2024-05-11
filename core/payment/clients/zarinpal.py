from django.contrib.sites.models import Site
from django.conf import settings
import requests
from .bank import BaseBank


class ZarinPalSandbox(BaseBank):
    MERCHANT_ID = settings.ZARINPAL_MERCHANT_ID
    CALLBACK_URL = f"http://{Site.objects.get_current().domain}/payment/verify/zp/"
    ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
    ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
    ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"

    def send_request(self, amount, description="پرداخت"):
        response = requests.post(
            url=self.ZP_API_REQUEST,
            json={
                'MerchantID': self.MERCHANT_ID,
                'Amount': int(amount),
                'CallbackURL': self.CALLBACK_URL,
                'Description': description,
            }
        )
        return response.json()

    def verify_payment(self, authority, amount):
        response = requests.post(
            url=self.ZP_API_VERIFY,
            json={
                "MerchantID": self.MERCHANT_ID,
                "Authority": authority,
                "Amount": int(amount),
            }
        )
        return response.json()

    def generate_payment_url(self, authority):
        return self.ZP_API_STARTPAY + authority
