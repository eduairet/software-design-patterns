# SOLID Design Principles

- Set of design principles introduced by Robert C. Martin in early 2000s.

## Single Responsibility Principle (SRP) or Separation of Concerns (SoC)

- A class should have only one reason to change or a class should have only one responsibility.

  ```py
  # This class has the only responsibility of managing the entries of a journal.
  class Journal:
      def __init__(self):
          self.entries = []
          self.count = 0

      def add_entry(self, text):
          self.entries.append(f"{self.count}: {text}")
          self.count += 1

      def remove_entry(self, pos):
          del self.entries[pos]

      def __str__(self):
          return "\n".join(self.entries)

      # If we want to save the entries to a file, we should create a separate class to avoid breaking the SRP.

  class PersistenceManager:
      @staticmethod
      def save_to_file(journal, filename):
          with open(filename,
                    "w") as file:
              file.write(str(journal))
  ```

- Making a class doing to much can lead to an anti-pattern called "God Object", which is a class that knows too much or does too much.

## Open/Closed Principle (OCP)

- This basically means that a class should be open for extension but closed for modification.

  ```py
  from enum import Enum

  class Color(Enum):
      RED = 1
      GREEN = 2
      BLUE = 3

  class Size(Enum):
      SMALL = 1
      MEDIUM = 2
      LARGE = 3

  class Product:
      def __init__(self, name, color, size):
          self.name = name
          self.color = color
          self.size = size

  class ProductFilter:
      @staticmethod
      def filter_by_color(products, color):
          for product in products:
              if product.color == color:
                  yield product

      @staticmethod
      def filter_by_size(products, size):
          for product in products:
              if product.size == size:
                  yield product

  # If we want to filter by both color and size, we have to modify the ProductFilter class.
  # This breaks the OCP and creates a problem called "State Space Explosion" where we have to create a new method for each combination of filters.
  ```

- To solve this problem, we can use the Specification Pattern.

  ```py
  class Specification:
      def is_satisfied(self, item):
          pass

      def __and__(self, other):
          return AndSpecification(self, other)


  class Filter:
      def filter(self, items, spec):
          pass


  class ColorSpecification(Specification):
      def __init__(self, color):
          self.color = color

      def is_satisfied(self, item):
          return item.color == self.color


  class SizeSpecification(Specification):
      def __init__(self, size):
          self.size = size

      def is_satisfied(self, item):
          return item.size == self.size


  class AndSpecification(Specification):
      def __init__(self, *args):
          self.args = args

      def is_satisfied(self, item):
          return all(map(
              lambda spec: spec.is_satisfied(item), self.args))


  class BetterFilter(Filter):
      def filter(self, items, spec):
          for item in items:
              if spec.is_satisfied(item):
                  yield item

  bf = BetterFilter()

  print('Green products:')
  green = ColorSpecification(Color.GREEN)
  for p in bf.filter(products, green):
      print(f' - {p.name} is green')

  print('Large products:')
  large = SizeSpecification(Size.LARGE)
  for p in bf.filter(products, large):
      print(f' - {p.name} is large')

  print('Large blue items:')
  # Here's the and specification in action, more clean and readable.
  large_blue = large & ColorSpecification(Color.BLUE)
  for p in bf.filter(products, large_blue):
      print(f' - {p.name} is large and blue')
  ```
