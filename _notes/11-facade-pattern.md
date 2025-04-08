# Façade Pattern

- Exposes several components through a single interface.
- Provides a simple, easy to understand/use interface over a complex subsystem.

  ```Python
  from random import randint


  class Generator:
      def generate(self, count):
          return [randint(1, 9) for x in range(count)]


  class Splitter:
      def split(self, array):
          result = []

          row_count = len(array)
          col_count = len(array[0])

          for r in range(row_count):
              the_row = []
              for c in range(col_count):
                  the_row.append(array[r][c])
              result.append(the_row)

          for c in range(col_count):
              the_col = []
              for r in range(row_count):
                  the_col.append(array[r][c])
              result.append(the_col)

          diag1 = []
          diag2 = []

          for c in range(col_count):
              for r in range(row_count):
                  if c == r:
                      diag1.append(array[r][c])
                  r2 = row_count - r - 1
                  if c == r2:
                      diag2.append(array[r][c])

          result.append(diag1)
          result.append(diag2)

          return result


  class Verifier:
      def verify(self, arrays):
          first = sum(arrays[0])

          for i in range(1, len(arrays)):
              if sum(arrays[i]) != first:
                  return False

          return True


  class MagicSquareGenerator:
      def generate(self, size):
          g, s, v = Generator(), Splitter(), Verifier()
          is_magic_square = False

          while not is_magic_square:
              magic_square = [g.generate(size) for _ in range(size)]
              arrays = s.split(magic_square)
              is_magic_square = v.verify(arrays)

          return magic_square
  ```
