# Singleton Pattern

- This is presumably the most hated design pattern because it is often misused.
- The Singleton pattern is used to ensure that a class has only one instance and provides a global point of access to that instance, like a database repository or an object factory.
- It's wise to use it when the initializer call is expensive and you want to share the same instance.
- We only call it once and we prevent the creation of multiple instances.
- Need to take car of lazy instantiation, thread safety, and multiple instances.

## Example

- We can use a class variable to store the instance and a class method to create the instance.

  ```python
  class Singleton:
      _instance = None

      def __new__(cls):
          if not cls._instance:
              cls._instance = super(Singleton, cls).__new__(cls)
              cls._instance.__initialized = False
          return cls._instance

      def __init__(self):
          if not self.__initialized:
              self.__initialized = True
              print('Singleton instance created')

  s1 = Singleton()
  s2 = Singleton()

  print(s1 == s2) # True
  ```

- We can also use a decorator to create a singleton.

  ```python
  def singleton(cls):
      instances = {}
      def get_instance(*args, **kwargs):
          if cls not in instances:
              instances[cls] = cls(*args, **kwargs)
          return instances[cls]
      return get_instance

  @singleton
  class Singleton:
      def __init__(self):
          print('Singleton instance created')

  s1 = Singleton()
  s2 = Singleton()

  print(s1 == s2) # True
  ```

- We can also use a metaclass to create a singleton.

  ```python
  class SingletonMeta(type):
      _instances = {}
      def __call__(cls, *args, **kwargs):
          if cls not in cls._instances:
              cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
          return cls._instances[cls]


  class Singleton(metaclass=SingletonMeta):
      def __init__(self):
          print('Singleton instance created')

  s1 = Singleton()
  s2 = Singleton()

  print(s1 == s2) # True
  ```

- A common concept in the Singleton pattern is the monostate, where all instances share the same state.

  ```python
  class CEO:
      __shared_state = {
          'name': 'Steve',
          'age': 55
      }

      def __init__(self):
          self.__dict__ = self.__shared_state

      def __str__(self):
          return f'{self.name} is {self.age} years old'


  class Monostate:
      _shared_state = {}

      def __new__(cls, *args, **kwargs):
          obj = super(Monostate, cls).__new__(cls, *args, **kwargs)
          obj.__dict__ = cls._shared_state
          return obj


  class CFO(Monostate):
      def __init__(self):
          self.name = ''
          self.money_managed = 0

      def __str__(self):
          return f'{self.name} manages ${self.money_managed}bn'

  if __name__ == '__main__':
      ceo1 = CEO()
      print(ceo1) # Steve is 55 years old

      ceo1.age = 66

      ceo2 = CEO()
      ceo2.age = 77
      print(ceo1) # Steve is 77 years old
      print(ceo2) # Steve is 77 years old

      ceo2.name = 'Tim'

      ceo3 = CEO()
      print(ceo1, ceo2, ceo3) # Tim is 77 years old

      cfo1 = CFO()
      cfo1.name = 'Sheryl'
      cfo1.money_managed = 1

      print(cfo1) # Sheryl manages $1bn

      cfo2 = CFO()
      cfo2.name = 'Ruth'
      cfo2.money_managed = 10
      print(cfo1, cfo2, sep='\n') # Ruth manages $10bn
  ```

## Testability

- The Singleton pattern is hard to test because it's hard to replace the instance with a mock object.
- We can use a factory to create the instance and a singleton to manage the instance.

  ```python
  import unittest


  class Singleton(type):
      _instances = {}

      def __call__(cls, *args, **kwargs):
          if cls not in cls._instances:
              cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
          return cls._instances[cls]


  class Database(metaclass=Singleton):
      def __init__(self):
          self.population = {}
          f = open('capitals.txt', 'r')
          lines = f.readlines()
          for i in range(0, len(lines), 2):
              self.population[lines[i].strip()] = int(lines[i + 1].strip())
          f.close()


  class SingletonRecordFinder:
      def total_population(self, cities):
          result = 0
          for c in cities:
              result += Database().population[c]
          return result


  class ConfigurableRecordFinder:
      def __init__(self, db):
          self.db = db

      def total_population(self, cities):
          result = 0
          for c in cities:
              result += self.db.population[c]
          return result


  class DummyDatabase:
      population = {
          'alpha': 1,
          'beta': 2,
          'gamma': 3
      }

      def get_population(self, name):
          return self.population[name]

  class SingletonTests(unittest.TestCase):
      def test_is_singleton(self):
          db = Database()
          db2 = Database()
          self.assertEqual(db, db2)

      def test_singleton_total_population(self):
          """ This tests on a live database :( """
          rf = SingletonRecordFinder()
          names = ['Seoul', 'Mexico City']
          tp = rf.total_population(names)
          self.assertEqual(tp, 17500000 + 17400000)  # what if these change?

      ddb = DummyDatabase()

      def test_dependent_total_population(self):
          crf = ConfigurableRecordFinder(self.ddb)
          self.assertEqual(
              crf.total_population(['alpha', 'beta']),
              3
          )

  if __name__ == '__main__':
      unittest.main()
  ```
