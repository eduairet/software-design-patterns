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

## Liskov Substitution Principle (LSP)

- Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program.

  ```py
  class Rectangle:
      def __init__(self, width, height):
          self._width = width
          self._height = height

      @property
      def width(self):
          return self._width

      @width.setter
      def width(self, value):
          self._width = value

      @property
      def height(self):
          return self._height

      @height.setter
      def height(self, height):
        self._height = height

      @property
      def area(self):
          return self._width * self._height

      def __str__(self):
          return f"Width: {self.width} | Height: {self.height}"

  # This class breaks the LSP because a square is a rectangle but the setters of the Rectangle class break the square properties.
  class Square(Rectangle):
      def __init__(self, size):
          super().__init__(size, size)

      @Rectangle.width.setter
      def width(self, value):
          self._width = self._height = value

      @Rectangle.height.setter
      def height(self, value):
          self._width = self._height = value
  ```

## Interface Segregation Principle (ISP)

- You don't want to stick too many methods in an interface.

  ```py
  # This class breaks the ISP because not all machines can fax or scan.
  class Machine:
      def print(self, document):
          pass

      def fax(self, document):
          pass

      def scan(self, document):
          pass

  # This interface is better because it's specific to the machines that can print, fax and scan.
  class MultiFunctionPrinter(Machine):
      def print(self, document):
          pass

      def fax(self, document):
          pass

      def scan(self, document):
          pass

  # This class breaks the ISP because old fashioned printers can't fax or scan.
  class OldFashionedPrinter(Machine):
      def print(self, document):
          pass

      def fax(self, document):
          pass

      def scan(self, document):
          pass
  ```

- To solve this problem, we can use the Interface Segregation Principle.

  ```py
  class Printer:
      @abstractmethod
      def print(self, document):
          pass

  class Scanner:
      @abstractmethod
      def scan(self, document):
          pass

  class Fax:
      @abstractmethod
      def fax(self, document):
          pass

  class MultiFunctionDevice(Printer, Scanner, Fax):
      def __init__(self):
          self.printer = Printer()
          self.scanner = Scanner()
          self.fax = Fax()

      def print(self, document):
          self.printer.print(document)

      def scan(self, document):
          self.scanner.scan(document)

      def fax(self, document):
          self.fax.fax(document)
  ```

## Dependency Inversion Principle (DIP)

- It's not related to dependency injection.
- High-level modules should not depend on low-level modules. Both should depend on abstractions.

  ```py
  from abc import abstractmethod
  from enum import Enum


  class Relationship(Enum):
      PARENT = 0
      CHILD = 1
      SIBLING = 2


  class Person:
      def __init__(self, name):
          self.name = name


  class RelationshipBrowser:
      @abstractmethod
      def find_all_children_of(self, name): pass


  class Relationships(RelationshipBrowser):  # low-level
      relations = []

      def add_parent_and_child(self, parent, child):
          self.relations.append((parent, Relationship.PARENT, child))
          self.relations.append((child, Relationship.PARENT, parent))

      def find_all_children_of(self, name):
          for r in self.relations:
              if r[0].name == name and r[1] == Relationship.PARENT:
                  yield r[2].name


  class Research:
      def __init__(self, browser):
          for p in browser.find_all_children_of("John"):
              print(f'John has a child called {p}')


  parent = Person('John')
  child1 = Person('Chris')
  child2 = Person('Matt')

  # low-level module
  relationships = Relationships()
  relationships.add_parent_and_child(parent, child1)
  relationships.add_parent_and_child(parent, child2)

  Research(relationships)
  ```

- In this example, the Research class is a high-level module and the Relationships class is a low-level module. The Research class should not depend on the Relationships class directly. Instead, it should depend on an abstraction that the Relationships class implements. In this case, the RelationshipBrowser class is the abstraction that the Relationships class implements.

## Sumary

- **Single Responsibility Principle (SRP):** A class should have only one reason to change or a class should have only one responsibility.
- **Open/Closed Principle (OCP):** A class should be open for extension but closed for modification.
- **Liskov Substitution Principle (LSP):** Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program.
- **Interface Segregation Principle (ISP):** You don't want to stick too many methods in an interface.
- **Dependency Inversion Principle (DIP):** High-level modules should not depend on low-level modules. Both should depend on abstractions.
