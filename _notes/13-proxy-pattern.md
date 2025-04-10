# Proxy Pattern

- A class that functions as an interface to another class.
- The class that is being proxied can be remote, expensive to create, or might need logging or additional functionality.

## Protection Proxy

- Controls access to the real subject and can add additional functionality and security.

  ```Python
  class Car:
      def __init__(self, driver):
          self.driver = driver

      def drive(self):
          print(f'Car being driven by {self.driver.name}')

  class CarProxy:
      def __init__(self, driver):
          self.driver = driver
          self.car = Car(driver)

      def drive(self):
          if self.driver.age >= 16:
              self.car.drive()
          else:
              print('Driver too young')


  class Driver:
      def __init__(self, name, age):
          self.name = name
          self.age = age


  car = CarProxy(Driver('John', 12))
  car.drive()
  ```

## Virtual Proxy

- A placeholder for a resource that is expensive to create.

  ```Python
  class Bitmap:
      def __init__(self, filename):
          self.filename = filename
          print(f'Loading image from {filename}')

      def draw(self):
          print(f'Drawing image {self.filename}')


  class LazyBitmap:
      def __init__(self, filename):
          self.filename = filename
          self.bitmap = None

      def draw(self):
          if not self.bitmap:
              self.bitmap = Bitmap(self.filename)
          self.bitmap.draw()

  def draw_image(image):
      print('About to draw image')
      image.draw()
      print('Done drawing image')


  bmp = LazyBitmap('facepalm.jpg')  # Bitmap
  draw_image(bmp)
  ```
