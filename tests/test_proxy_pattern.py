from software_design_patterns.structural.proxy_pattern import *


def test_proxy_escrow():
    BUYER = "Jonaz"
    SELLER = "Simpson"
    PAYMENT = 100
    EXPECTED_ESCROW = (
        f"Payment of ${PAYMENT} is held in escrow. Waiting for buyer approval."
    )
    EXPECTED_RELEASE = (
        f"Buyer {BUYER} has approved the payment. Releasing funds to {SELLER}."
    )
    EXPECTED_PROCESS = f"Payment of ${PAYMENT} sent to {SELLER}."

    escrow = EscrowProxy(buyer=BUYER, seller=SELLER)

    assert escrow.process_payment(PAYMENT) == EXPECTED_ESCROW
    assert escrow.payment_released is False
    assert escrow.release_payment() == EXPECTED_RELEASE
    assert escrow.payment_released is True
    assert escrow.process_payment(PAYMENT) == EXPECTED_PROCESS
