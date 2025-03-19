# Factory Pattern

- Ideal when object creation is complex and the initializer is not descriptive.
- The object creation is outsourced (non-piecewise like in the builder pattern) to a factory method.
- **Factory** is a component responsible solely for the wholesale (not piecewise) creation of objects.

## Examples

- Factory method

  ```py
  class Point:
      def __init__(self, x, y):
          self.x = x
          self.y = y

      def __create_cartesian_point(self, x, y):
          self.x = x
          self.y = y

      def __create_polar_point(self, rho, theta):
          self.x = rho * math.cos(theta)
          self.y = rho * math.sin(theta)
  ```

  - Instead of having a constructor with multiple parameters, we can have multiple factory methods.

- Factory class

  ```py
  class PointFactory:
      @staticmethod
      def new_cartesian_point(x, y):
          return Point(x, y)

      @staticmethod
      def new_polar_point(rho, theta):
          return Point(rho * math.cos(theta), rho * math.sin(theta))
  ```

  - In this case we outsource the creation of the object to a factory class.

- Abstract Factory

  ```py
  from abc import ABC
  from enum import Enum, auto


  class HotDrink(ABC):
      def consume(self):
          pass


  class Tea(HotDrink):
      def consume(self):
          print('This tea is nice but I\'d prefer it with milk')


  class Coffee(HotDrink):
      def consume(self):
          print('This coffee is delicious')


  class TeaFactory:
      def prepare(self, amount):
          print(f'Put in tea bag, boil water, pour {amount}ml, enjoy!')
          return Tea()


  class CoffeeFactory:
      def prepare(self, amount):
          print(f'Grind some beans, boil water, pour {amount}ml, enjoy!')
          return Coffee()


  class HotDrinkMachine:
      class AvailableDrink(Enum):  # violates OCP
          COFFEE = auto()
          TEA = auto()

      factories = []
      initialized = False

      def __init__(self):
          if not self.initialized:
              self.initialized = True
              for d in self.AvailableDrink:
                  name = d.name[0] + d.name[1:].lower()
                  factory_name = name + 'Factory'
                  factory_instance = eval(factory_name)()
                  self.factories.append((name, factory_instance))

      def make_drink(self):
          print('Available drinks:')
          for f in self.factories:
              print(f[0])

          s = input(f'Please pick drink (0-{len(self.factories)-1}): ')
          idx = int(s)
          s = input(f'Specify amount: ')
          amount = int(s)
          return self.factories[idx][1].prepare(amount)


  if __name__ == '__main__':
      hdm = HotDrinkMachine()
      drink = hdm.make_drink()
      drink.consume()
  ```
