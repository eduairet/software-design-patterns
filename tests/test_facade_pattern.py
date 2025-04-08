from software_design_patterns.structural.facade_pattern import *
import pytest


TO = "test@test.com"
SUBJECT = "Test Subject"
BODY = "Test Body"


def test_facade_email():

    email_client = EmailFacade(smtp_server=GmailServer())
    email_client.connect()

    assert email_client.smtp_server.connected is True
    assert email_client.smtp_server.authenticated is True
    assert len(email_client.smtp_server.mailbox) == 0

    email_client.send_email(TO, SUBJECT, BODY)

    assert len(email_client.smtp_server.mailbox) == 1
    assert email_client.smtp_server.mailbox[0].to == TO
    assert email_client.smtp_server.mailbox[0].subject == SUBJECT
    assert email_client.smtp_server.mailbox[0].body == BODY
    assert email_client.smtp_server.connected is False
    assert email_client.smtp_server.authenticated is False


def test_facade_email_fail():
    email_client = EmailFacade(smtp_server=GmailServer())

    with pytest.raises(Exception, match="Not connected or authenticated"):
        email_client.send_email(TO, SUBJECT, BODY)
