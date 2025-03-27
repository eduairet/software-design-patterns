# Adapter Pattern

- It tries to make two incompatible interfaces compatible. It is a structural pattern.

  ```Python
  class Point:
      def __init__(self, x, y):
          self.y = y
          self.x = x


  def draw_point(p):
      print(".", end="")


  class Line:
      def __init__(self, start, end):
          self.end = end
          self.start = start


  class Rectangle(list):
      def __init__(self, x, y, width, height):
          super().__init__()
          self.append(Line(Point(x, y), Point(x + width, y)))
          self.append(Line(Point(x + width, y), Point(x + width, y + height)))
          self.append(Line(Point(x, y), Point(x, y + height)))
          self.append(Line(Point(x, y + height), Point(x + width, y + height)))


  class LineToPointAdapter(list):
      count = 0

      def __init__(self, line):
          self.count += 1
          print(
              f"{self.count}: Generating points for line "
              f"[{line.start.x},{line.start.y}]→"
              f"[{line.end.x},{line.end.y}]"
          )

          left = min(line.start.x, line.end.x)
          right = max(line.start.x, line.end.x)
          top = min(line.start.y, line.end.y)
          bottom = min(line.start.y, line.end.y)

          if right - left == 0:
              for y in range(top, bottom):
                  self.append(Point(left, y))
          elif line.end.y - line.start.y == 0:
              for x in range(left, right):
                  self.append(Point(x, top))


  def draw(rcs):
      print("\n\n--- Drawing some stuff ---\n")
      for rc in rcs:
          for line in rc:
              adapter = LineToPointAdapter(line)
              for p in adapter:
                  draw_point(p)


  rs = [Rectangle(1, 1, 10, 10), Rectangle(3, 3, 6, 6)]

  draw(rs)
  """

  --- Drawing some stuff ---

  1: Generating points for line [1,1]→[11,1]
  ..........1: Generating points for line [11,1]→[11,11]
  1: Generating points for line [1,1]→[1,11]
  1: Generating points for line [1,11]→[11,11]
  ..........1: Generating points for line [3,3]→[9,3]
  ......1: Generating points for line [9,3]→[9,9]
  1: Generating points for line [3,3]→[3,9]
  1: Generating points for line [3,9]→[9,9]
  ......
  """

  draw(rs) # This will generate the same points again.
  ```

- To make an adapter more efficient we can use a caching mechanism.

  ```Python
  class LineToPointAdapter(list):
      count = 0
      cache = {}

      def __init__(self, line):
          self.h = hash(line)
          if self.h in self.cache:
              return

          super().__init__()
          self.count += 1

          print(
              f"{self.count}: Generating points for line "
              f"[{line.start.x},{line.start.y}]→"
              f"[{line.end.x},{line.end.y}]"
          )

          left = min(line.start.x, line.end.x)
          right = max(line.start.x, line.end.x)
          top = min(line.start.y, line.end.y)
          bottom = min(line.start.y, line.end.y)

          points = []

          if right - left == 0:
              for y in range(top, bottom):
                  points.append(Point(left, y))
          elif line.end.y - line.start.y == 0:
              for x in range(left, right):
                  points.append(Point(x, top))

          self.cache[self.h] = points

      def __iter__(self):
          return iter(self.cache[self.h])
  ```

  - This way the second time we try to generate points for the same line, we will get the points from the cache and it will only show the line.

    ```Python
    draw(rs)
    """

    --- Drawing some stuff ---

    1: Generating points for line [1,1]→[11,1]
    ..........1: Generating points for line [11,1]→[11,11]
    1: Generating points for line [1,1]→[1,11]
    1: Generating points for line [1,11]→[11,11]
    ..........1: Generating points for line [3,3]→[9,3]
    ......1: Generating points for line [9,3]→[9,9]
    1: Generating points for line [3,3]→[3,9]
    1: Generating points for line [3,9]→[9,9]
    ......
    """

    draw(rs)
    """

    --- Drawing some stuff ---

    ................................
    """
    ```
