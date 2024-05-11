from abc import ABC, abstractmethod

class BaseBank(ABC):

    @abstractmethod
    def send_request(self, amount, description):
        pass

    @abstractmethod
    def verify_payment(self, authority, amount):
        pass

    @abstractmethod
    def generate_payment_url(self, authority):
        pass
