# Flyweight Pattern

- It's a space optimization pattern that is used to minimize memory usage by sharing common parts of state between multiple objects.

  ```Python
  class User:
      strings = []

      def __init__(self, full_name):
          def get_or_add(s):
              if s in self.strings:
                  return self.strings.index(s)
              else:
                  self.strings.append(s)
                  return len(self.strings)-1
          self.names = [get_or_add(x) for x in full_name.split(' ')]

      def __str__(self):
          return ' '.join([self.strings[x] for x in self.names])


  def random_string():
      chars = string.ascii_lowercase
      return ''.join([random.choice(chars) for x in range(8)])

  u1 = User('Luis Rodriguez')
  u2 = User('Samuel Rodriguez')
  print(u1.names) # [0, 1]
  print(u2.names) # [2, 1]
  print(User.strings) # ['Luis', 'Rodriguez', 'Samuel']

  users = []

  for first in first_names:
      for last in last_names:
          users.append(User(f'{first} {last}'))

  # This approaches helps to save memory by sharing the common strings
  ```

- A good example of the Flyweight pattern is a text editor that allows you to format text. The text editor can use the Flyweight pattern to share the formatting information for different parts of the text, rather than creating a separate object for each part of the text.

  ```Python
  class FormattedText:
      def __init__(self, plain_text):
          self.plain_text = plain_text
          self.formatting = []

      class TextRange:
          def __init__(self, start, end, capitalize=False, bold=False, italic=False):
              self.end = end
              self.bold = bold
              self.capitalize = capitalize
              self.italic = italic
              self.start = start

          def covers(self, position):
              return self.start <= position <= self.end

      def get_range(self, start, end):
          range = self.TextRange(start, end)
          self.formatting.append(range)
          return range

      def __str__(self):
          result = []
          for i in range(len(self.plain_text)):
              c = self.plain_text[i]
              for r in self.formatting:
                  if r.covers(i) and r.capitalize:
                      c = c.upper()
              result.append(c)
          return ''.join(result)


  formatted_text = FormattedText('This is a brave new world')
  formatted_text.get_range(16, 19).capitalize = True
  print(formatted_text) # This is a BRAVE new world
  ```
