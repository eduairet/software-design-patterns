from software_design_patterns.behavioral.chain_of_responsibility_pattern import *


def test_chain_of_responsibility_support():
    basic_support = BasicSupport()
    advanced_support = AdvancedSupport()
    manager_support = ManagerSupport()

    basic_support.set_next(advanced_support).set_next(manager_support)

    issues, expected_responses = [
        SupportLevel.PASSWORD_RESET.value,
        SupportLevel.ACCOUNT_RECOVERY.value,
        SupportLevel.BILLING_DISPUTE.value,
        "unknown issue",
    ], [
        "Basic Support: Resolved 'password reset' issue.",
        "Advanced Support: Resolved 'account recovery' issue.",
        "Manager Support: Resolved 'billing dispute' issue.",
        "The issue could not be resolved. Escalating to external support.",
    ]

    for issue, expected_response in zip(issues, expected_responses):
        assert basic_support.handle_request(issue) == expected_response
