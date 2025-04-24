# Memento Pattern

- It's a token/handle that represents the system state and lets you restore it later.
- It can or cannot be exposed to state information.

  ```Python
  class Memento:
      def __init__(self, balance):
          self.balance = balance


  class BankAccount:
      def __init__(self, balance=0):
          self.balance = balance


      def deposit(self, amount):
          self.balance += amount
          return Memento(self.balance)

      def restore(self, memento):
          self.balance = memento.balance

      def __str__(self):
          return f'Balance = {self.balance}'


  ba = BankAccount(100)
  m1 = ba.deposit(50)
  m2 = ba.deposit(25)
  print(ba)

  # restore to m1
  ba.restore(m1)
  print(ba)

  # restore to m2
  ba.restore(m2)
  print(ba)
  ```

- In the previous example the memento doesn't have exposition to the initial state, if we need to expose the state, and also allow undo/redo, we can do it like this:

  ```Python
  class Memento:
      def __init__(self, balance):
          self.balance = balance


  class BankAccount:
      def __init__(self, balance=0):
          self.balance = balance
          self.changes = [Memento(self.balance)]
          self.current = 0


      def deposit(self, amount):
          self.balance += amount
          m = Memento(self.balance)
          self.changes.append(m)
          self.current += 1
          return m

      def restore(self, memento):
          if memento:
              self.balance = memento.balance
              self.changes.append(memento)
              self.current = len(self.changes)-1

      def undo(self):
          if self.current > 0:
              self.current -= 1
              m = self.changes[self.current]
              self.balance = m.balance
              return m
          return None

      def redo(self):
          if self.current + 1 < len(self.changes):
              self.current += 1
              m = self.changes[self.current]
              self.balance = m.balance
              return m
          return None

      def __str__(self):
          return f'Balance = {self.balance}'


  ba = BankAccount(100)
  ba.deposit(50)
  ba.deposit(25)
  print(ba)

  ba.undo()
  print(f'Undo 1: {ba}')
  ba.undo()
  print(f'Undo 2: {ba}')
  ba.redo()
  print(f'Redo 1: {ba}')
  ```
