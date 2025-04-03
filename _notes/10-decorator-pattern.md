# Decorator Pattern

- The decorator pattern allows to add new functionality to an object without altering its structure.
- Functional decorators

  ```python
  import time

  def time_it(func):
    def wrapper():
      start = time.time()
      result = func()
      end = time.time()
      print(f'{func.__name__} took {int((end-start)*1000)}ms')
    return wrapper


  def some_op():
    print('Starting op')
    time.sleep(1)
    print('We are done')
    return 123

  time_it(some_op)() # Here we are calling the decorator function
  ```

  - We can also add the functionality from `time_it` to the function `some_op` without modifying the function itself using an @ decorator, this is a syntactic sugar for the previous example and is the most common way to use decorators in Python.

    ```python
    import time

    def time_it(func):
      def wrapper():
        start = time.time()
        result = func()
        end = time.time()
        print(f'{func.__name__} took {int((end-start)*1000)}ms')
      return wrapper

    @time_it # This implements the functionality from time_it to the function
    def some_op():
      print('Starting op')
      time.sleep(1)
      print('We are done')
      return 123
    ```

- Classic decorator

  ```Python
  from abc import ABC


  class Shape(ABC):
      def __str__(self):
          return ''


  class Circle(Shape):
      def __init__(self, radius=0.0):
          self.radius = radius

      def resize(self, factor):
          self.radius *= factor

      def __str__(self):
          return f'A circle of radius {self.radius}'


  class Square(Shape):
      def __init__(self, side):
          self.side = side

      def __str__(self):
          return f'A square with side {self.side}'


  class ColoredShape(Shape):
      def __init__(self, shape, color):
          if isinstance(shape, ColoredShape):
              raise Exception('Cannot apply ColoredDecorator twice')
          self.shape = shape
          self.color = color

      def __str__(self):
          return f'{self.shape} has the color {self.color}'


  class TransparentShape(Shape):
      def __init__(self, shape, transparency):
          self.shape = shape
          self.transparency = transparency

      def __str__(self):
          return f'{self.shape} has {self.transparency * 100.0}% transparency'


  circle = Circle(2)
  print(circle)

  red_circle = ColoredShape(circle, "red")
  print(red_circle) # A circle of radius 2 has the color red

  red_half_transparent_square = TransparentShape(red_circle, 0.5)
  print(red_half_transparent_square) # A circle of radius 2 has the color red has 50.0% transparency

  mixed = ColoredShape(ColoredShape(Circle(3), 'red'), 'blue') # This will raise the exception
  ```

- Dynamic decorator

  ```Python
  class FileWithLogging:
    def __init__(self, file):
      self.file = file

    def writelines(self, strings):
      self.file.writelines(strings)
      print(f'wrote {len(strings)} lines')

    def __iter__(self):
      return self.file.__iter__()

    def __next__(self):
      return self.file.__next__()

    def __getattr__(self, item):
      return getattr(self.__dict__['file'], item)

    def __setattr__(self, key, value):
      if key == 'file':
        self.__dict__[key] = value
      else:
        setattr(self.__dict__['file'], key)

    def __delattr__(self, item):
      delattr(self.__dict__['file'], item)


  file = FileWithLogging(open('hello.txt', 'w'))
  file.writelines(['hello', 'world']) # This will write hello and world to the file and log the number of lines written thanks to the decorator
  file.write('testing')
  file.close()
  ```
