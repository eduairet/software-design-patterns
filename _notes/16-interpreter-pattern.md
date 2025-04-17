# Interpreter Pattern

- It's helpful when you need to evaluate or interpret a language or expression.
- Some examples are:

  - Programming languages compilers, interpreters, and parsers.
  - HTML, XML, and similars
  - Numerical expressions (e.g., 1 + 2 × 3)
  - Regular expressions

- The interpreter turns strings into objects and vice versa.

- Lexing

  - The process of breaking a string into tokens.
  - A token is a string with a specific meaning.

  ```Python
  from enum import Enum


  class Token:
      class Type(Enum):
          INTEGER = 0
          PLUS = 1
          MINUS = 2
          LPAREN = 3
          RPAREN = 4

      def __init__(self, type, text):
          self.type = type
          self.text = text

      def __str__(self):
          return f'`{self.text}`'


  def lex(input):
      result = []

      i = 0
      while i < len(input):
          if input[i] == '+':
              result.append(Token(Token.Type.PLUS, '+'))
          elif input[i] == '-':
              result.append(Token(Token.Type.MINUS, '-'))
          elif input[i] == '(':
              result.append(Token(Token.Type.LPAREN, '('))
          elif input[i] == ')':
              result.append(Token(Token.Type.RPAREN, ')'))
          else:  # must be a number
              digits = [input[i]]
              for j in range(i + 1, len(input)):
                  if input[j].isdigit():
                      digits.append(input[j])
                      i += 1
                  else:
                      result.append(Token(Token.Type.INTEGER, ''.join(digits)))
                      break
          i += 1

      return result
  ```

- Parsing

  - The process of turning a list of tokens into an expression tree.

  ```Python
  class Integer:
      def __init__(self, value):
          self.value = value


  class BinaryOperation:
      class Type(Enum):
          ADDITION = 0
          SUBTRACTION = 1

      def __init__(self):
          self.type = None
          self.left = None
          self.right = None

      @property
      def value(self):
          if self.type == self.Type.ADDITION:
              return self.left.value + self.right.value
          elif self.type == self.Type.SUBTRACTION:
              return self.left.value - self.right.value


  def parse(tokens):
      result = BinaryOperation()
      have_lhs = False
      i = 0
      while i < len(tokens):
          token = tokens[i]

          if token.type == Token.Type.INTEGER:
              integer = Integer(int(token.text))
              if not have_lhs:
                  result.left = integer
                  have_lhs = True
              else:
                  result.right = integer
          elif token.type == Token.Type.PLUS:
              result.type = BinaryOperation.Type.ADDITION
          elif token.type == Token.Type.MINUS:
              result.type = BinaryOperation.Type.SUBTRACTION
          elif token.type == Token.Type.LPAREN:
              j = i
              while j < len(tokens):
                  if tokens[j].type == Token.Type.RPAREN:
                      break
                  j += 1
              subexpression = tokens[i + 1:j]
              element = parse(subexpression)
              if not have_lhs:
                  result.left = element
                  have_lhs = True
              else:
                  result.right = element
              i = j
          i += 1
      return result

  def eval(input):
      tokens = lex(input)
      print(' '.join(map(str, tokens)))

      parsed = parse(tokens)
      print(f'{input} = {parsed.value}')


  eval('(13+4)-(12+1)') # `(` `13` `+` `4` `)` `-` `(` `1` `2` `+` `1` `)`\n(13+4)-(12+1) = 4
  eval('1+(3-4)') # `1` `+` `(` `3` `-` `4` `)`\n1+(3-4) = 0
  ```
