from enum import Enum


class SupportLevel(Enum):
    PASSWORD_RESET = "password reset"
    ACCOUNT_RECOVERY = "account recovery"
    BILLING_DISPUTE = "billing dispute"


class SupportHandler:
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler
        return handler

    def handle_request(self, issue):
        if self.next_handler:
            return self.next_handler.handle_request(issue)
        else:
            return "The issue could not be resolved. Escalating to external support."


class BasicSupport(SupportHandler):
    def handle_request(self, issue):
        can_solve_issue = issue == SupportLevel.PASSWORD_RESET.value
        return (
            f"Basic Support: Resolved '{SupportLevel.PASSWORD_RESET.value}' issue."
            if can_solve_issue
            else super().handle_request(issue)
        )


class AdvancedSupport(SupportHandler):
    def handle_request(self, issue):
        can_solve_issue = issue == SupportLevel.ACCOUNT_RECOVERY.value
        return (
            f"Advanced Support: Resolved '{SupportLevel.ACCOUNT_RECOVERY.value}' issue."
            if can_solve_issue
            else super().handle_request(issue)
        )


class ManagerSupport(SupportHandler):
    def handle_request(self, issue):
        can_solve_issue = issue == SupportLevel.BILLING_DISPUTE.value
        return (
            f"Manager Support: Resolved '{SupportLevel.BILLING_DISPUTE.value}' issue."
            if can_solve_issue
            else super().handle_request(issue)
        )
