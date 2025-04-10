from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass


class DirectPaymentProcessor(PaymentProcessor):
    def __init__(self, seller: str):
        self.seller = seller

    def process_payment(self, amount: float) -> str:
        return f"Payment of ${amount} sent to {self.seller}."


class EscrowProxy(PaymentProcessor):
    def __init__(self, buyer: str, seller: str):
        self.buyer = buyer
        self.seller = seller
        self.payment_processor = DirectPaymentProcessor(seller)
        self.payment_released = False

    def process_payment(self, amount: float) -> str:
        if self.payment_released:
            return self.payment_processor.process_payment(amount)
        else:
            return (
                f"Payment of ${amount} is held in escrow. Waiting for buyer approval."
            )

    def release_payment(self):
        self.payment_released = True
        return f"Buyer {self.buyer} has approved the payment. Releasing funds to {self.seller}."
