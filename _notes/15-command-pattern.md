# Command Pattern

- It's an object that represents a operation or action.
- Contains all the information needed to perform an action.
- Here's a simple example of a command pattern in Python:

  ```Python
  from abc import ABC
  from enum import Enum


  class BankAccount:
      OVERDRAFT_LIMIT = -500

      def __init__(self, balance=0):
          self.balance = balance

      def deposit(self, amount):
          self.balance += amount
          print(f'Deposited {amount}, balance = {self.balance}')

      def withdraw(self, amount):
          if self.balance - amount >= BankAccount.OVERDRAFT_LIMIT:
              self.balance -= amount
              print(f'Withdrew {amount}, balance = {self.balance}')
              return True
          return False

      def __str__(self):
          return f'Balance = {self.balance}'


  class Command(ABC):
      def invoke(self):
          pass

      def undo(self):
          pass


  class BankAccountCommand(Command):
      def __init__(self, account, action, amount):
          self.amount = amount
          self.action = action
          self.account = account
          self.success = None

      class Action(Enum):
          DEPOSIT = 0
          WITHDRAW = 1

      def invoke(self):
          if self.action == self.Action.DEPOSIT:
              self.account.deposit(self.amount)
              self.success = True
          elif self.action == self.Action.WITHDRAW:
              self.success = self.account.withdraw(self.amount)

      def undo(self):
          if not self.success:
              return
          # just for demo purposes
          if self.action == self.Action.DEPOSIT:
              self.account.withdraw(self.amount)
          elif self.action == self.Action.WITHDRAW:
              self.account.deposit(self.amount)


  ba = BankAccount()
  cmd = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 100)
  cmd.invoke() # Deposited 100, balance = 100
  print('After $100 deposit:', ba) # After $100 deposit: Balance = 100

  cmd.undo() # Withdrew 100, balance = 0
  print('$100 deposit undone:', ba) # $100 deposit undone: Balance = 0

  illegal_cmd = BankAccountCommand(ba, BankAccountCommand.Action.WITHDRAW, 1000)
  illegal_cmd.invoke() # Withdrew 1000, balance = -1000
  print('After impossible withdrawal:', ba) # After impossible withdrawal: Balance = 0
  illegal_cmd.undo() # False
  print('After undo:', ba) # After undo: Balance = 0
  ```

- Another way to construct a command with this pattern is with a composite command which is a command that contains other commands.

  ```Python
  import unittest
  from abc import ABC, abstractmethod
  from enum import Enum


  class BankAccount:
      OVERDRAFT_LIMIT = -500

      def __init__(self, balance=0):
          self.balance = balance

      def deposit(self, amount):
          self.balance += amount
          print(f"Deposited {amount}, balance = {self.balance}")

      def withdraw(self, amount):
          if self.balance - amount >= BankAccount.OVERDRAFT_LIMIT:
              self.balance -= amount
              print(f"Withdrew {amount}, balance = {self.balance}")
              return True
          return False

      def __str__(self):
          return f"Balance = {self.balance}"


  class Command(ABC):
      def __init__(self):
          self.success = False

      def invoke(self):
          pass

      def undo(self):
          pass


  class BankAccountCommand(Command):
      def __init__(self, account, action, amount):
          super().__init__()
          self.amount = amount
          self.action = action
          self.account = account

      class Action(Enum):
          DEPOSIT = 0
          WITHDRAW = 1

      def invoke(self):
          if self.action == self.Action.DEPOSIT:
              self.account.deposit(self.amount)
              self.success = True
          elif self.action == self.Action.WITHDRAW:
              self.success = self.account.withdraw(self.amount)

      def undo(self):
          if not self.success:
              return
          if self.action == self.Action.DEPOSIT:
              self.account.withdraw(self.amount)
          elif self.action == self.Action.WITHDRAW:
              self.account.deposit(self.amount)


  class CompositeBankAccountCommand(Command, list):
      def __init__(self, items=[]):
          super().__init__()
          for i in items:
              self.append(i)

      def invoke(self):
          for x in self:
              x.invoke()

      def undo(self):
          for x in reversed(self):
              x.undo()


  class MoneyTransferCommand(CompositeBankAccountCommand):
      def __init__(self, from_acct, to_acct, amount):
          super().__init__(
              [
                  BankAccountCommand(
                      from_acct, BankAccountCommand.Action.WITHDRAW, amount
                  ),
                  BankAccountCommand(to_acct, BankAccountCommand.Action.DEPOSIT, amount),
              ]
          )

      def invoke(self):
          ok = True
          for cmd in self:
              if ok:
                  cmd.invoke()
                  ok = cmd.success
              else:
                  cmd.success = False
          self.success = ok


  class TestSuite(unittest.TestCase):
      def test_composite_deposit(self):
          ba = BankAccount()
          deposit1 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 1000)
          deposit2 = BankAccountCommand(ba, BankAccountCommand.Action.DEPOSIT, 1000)
          composite = CompositeBankAccountCommand([deposit1, deposit2])
          composite.invoke()  # Deposited 1000, balance = 1000\nDeposited 1000, balance = 2000
          print(ba)  # Balance = 2000
          composite.undo()  # Withdrew 1000, balance = 1000\nWithdrew 1000, balance = 0
          print(ba)  # Balance = 0

      def test_transfer_fail(self):
          ba1 = BankAccount(100)
          ba2 = BankAccount()

          amount = 1000

          transfer = MoneyTransferCommand(ba1, ba2, amount)
          transfer.invoke()  # Nothing happened
          print("ba1:", ba1, "ba2:", ba2)  # ba1: Balance = 100 ba2: Balance = 0
          transfer.undo()  # Nothing happened
          print("ba1:", ba1, "ba2:", ba2)  # ba1: Balance = 100 ba2: Balance = 0
          print(transfer.success)  # False

      def test_better_tranfer(self):
          ba1 = BankAccount(100)
          ba2 = BankAccount()

          amount = 100

          transfer = MoneyTransferCommand(ba1, ba2, amount)
          transfer.invoke()  # Withdrew 100, balance = 0\nDeposited 100, balance = 100
          print("ba1:", ba1, "ba2:", ba2)  # ba1: Balance = 0 ba2: Balance = 100
          transfer.undo()  # Deposited 100, balance = 100\nWithdrew 100, balance = 0
          print("ba1:", ba1, "ba2:", ba2)  # ba1: Balance = 100 ba2: Balance = 0
          print(transfer.success)  # True
  ```
