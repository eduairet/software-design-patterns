from abc import ABC, abstractmethod


class EmailFacade:
    def __init__(self, smtp_server):
        self.smtp_server = smtp_server
        self.authenticator = Authenticator()
        self.message = Message()

    def connect(self):
        if not self.smtp_server.connected:
            self.smtp_server.connect()
            self.authenticator.login()
            self.smtp_server.authenticated = True

    def send_email(self, to, subject, body):
        self.message.create(to, subject, body)
        self.smtp_server.send(self.message)
        self.smtp_server.mailbox.append(self.message)
        self.smtp_server.disconnect()


class SmtpServer(ABC):
    def __init__(self):
        self._mailbox = []
        self._connected = False
        self._authenticated = False

    @property
    def mailbox(self):
        return self._mailbox

    @mailbox.setter
    def mailbox(self, mailbox):
        self._mailbox = mailbox

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, connected):
        self._connected = connected

    @property
    def authenticated(self):
        return self._authenticated

    @authenticated.setter
    def authenticated(self, authenticated):
        self._authenticated = authenticated

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def disconnect(self):
        pass


class GmailServer(SmtpServer):
    def connect(self):
        self.connected = True
        self.authenticated = True

    def send(self, message):
        if not self.connected or not self.authenticated:
            raise Exception("Not connected or authenticated")
        print(
            f"Sending email to {message.to} with subject '{message.subject}' and body '{message.body}'"
        )

    def disconnect(self):
        self.connected = False
        self.authenticated = False


class Authenticator:
    def __init__(self):
        self._authenticated = False

    @property
    def authenticated(self):
        return self._authenticated

    @authenticated.setter
    def authenticated(self, authenticated):
        self._authenticated = authenticated

    def login(self):
        self.authenticated = True


class Message:
    def create(self, to, subject, body):
        self.to = to
        self.subject = subject
        self.body = body
