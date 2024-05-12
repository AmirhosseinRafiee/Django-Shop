from django.contrib.sites.models import Site
from django.conf import settings
import requests
from .bank import BaseBank


class PayPingSandbox(BaseBank):
    TOKEN = settings.PAYPING_TOKEN
    CALLBACK_URL = f"http://{Site.objects.get_current().domain}/payment/verify/pp/"
    ZP_API_REQUEST = "https://api.payping.ir/v2/pay"
    ZP_API_VERIFY = "https://api.payping.ir/v2/pay/verify"
    ZP_API_STARTPAY = "https://api.payping.ir/v2/pay/gotoipg/"

    def send_request(self, amount, description="پرداخت"):
        response = requests.post(
            url=self.ZP_API_REQUEST,
            json={
                'amount': int(amount),
                'returnUrl': self.CALLBACK_URL,
                'description': description,
            },
            headers={
                'Authorization': 'Bearer ' + self.TOKEN
            }
        )
        return response

    def verify_payment(self, ref_id, amount):
        response = requests.post(
            url=self.ZP_API_VERIFY,
            json={
                "refId": ref_id,
                "amount": int(amount),
            },
            headers={
                'Authorization': 'Bearer ' + self.TOKEN
            }
        )
        return response

    def generate_payment_url(self, code):
        return self.ZP_API_STARTPAY + code
