# Visitor Pattern

- This pattern is used to define an entire new operation without changing the classes of the elements on which it operates.
- It is created by adding a component (Visitor) that knows how to traverse the structure of the object and perform operations on it.
- You can create an intrusive visitor that modifies the object structure, but this is not recommended since it violates the Open/Closed Principle.

  ```Python
  class DoubleExpression:
      def __init__(self, value):
          self.value = value

      def print(self, buffer):
          buffer.append(str(self.value))

      def eval(self):
          return self.value


  class AdditionExpression:
      def __init__(self, left, right):
          self.right = right
          self.left = left

      def print(self, buffer):
          buffer.append("(")
          self.left.print(buffer)
          buffer.append("+")
          self.right.print(buffer)
          buffer.append(")")

      def eval(self):
          return self.left.eval() + self.right.eval()


  # represents 1+(2+3)
  e = AdditionExpression(
      DoubleExpression(1), AdditionExpression(DoubleExpression(2), DoubleExpression(3))
  )
  buffer = []
  e.print(buffer)
  print("".join(buffer), "=", e.eval())  # (1+(2+3)) = 6
  ```

- A way to avoid being intrusive (still violating the Open/Closed Principle) is to use a reflective visitor, which is a visitor that does not modify the object structure but instead uses reflection to access the object structure.

  ```Python
  from abc import ABC


  class Expression(ABC):
      pass


  class DoubleExpression(Expression):
      def __init__(self, value):
          self.value = value


  class AdditionExpression(Expression):
      def __init__(self, left, right):
          self.right = right
          self.left = left


  class ExpressionPrinter:
      @staticmethod
      def print(e, buffer):
          if isinstance(
              e, DoubleExpression
          ):  # The tradeoff of this approach comes when the instance does not exist
              buffer.append(str(e.value))
          elif isinstance(e, AdditionExpression):
              buffer.append("(")
              ExpressionPrinter.print(e.left, buffer)
              buffer.append("+")
              ExpressionPrinter.print(e.right, buffer)
              buffer.append(")")

      Expression.print = lambda self, b: ExpressionPrinter.print(self, b)


  # represents 1+(2+3)
  e = AdditionExpression(
      DoubleExpression(1), AdditionExpression(DoubleExpression(2), DoubleExpression(3))
  )
  buffer = []
  e.print(buffer)
  print("".join(buffer))  # (1+(2+3))
  ```

- There's another way to create a visitor, which is actually the classic one, the double dispatch, where the visitor is a class that implements the visitor interface and the element is a class that implements the element interface. The visitor is passed to the element, which calls the appropriate method on the visitor. In python, we won't need the accept method, this is only necessary in languages that use static typing.

  ```Python
  # Visitor Pattern

  # taken from https://tavianator.com/the-visitor-pattern-in-python/


  def _qualname(obj):
      """Get the fully-qualified name of an object (including module)."""
      return obj.__module__ + "." + obj.__qualname__


  def _declaring_class(obj):
      """Get the name of the class that declared an object."""
      name = _qualname(obj)
      return name[: name.rfind(".")]


  # Stores the actual visitor methods
  _methods = {}


  # Delegating visitor implementation
  def _visitor_impl(self, arg):
      """Actual visitor method implementation."""
      method = _methods[(_qualname(type(self)), type(arg))]
      return method(self, arg)


  # The actual @visitor decorator
  def visitor(arg_type):
      """Decorator that creates a visitor method."""

      def decorator(fn):
          declaring_class = _declaring_class(fn)
          _methods[(declaring_class, arg_type)] = fn

          # Replace all decorated methods with _visitor_impl
          return _visitor_impl

      return decorator


  class DoubleExpression:
      def __init__(self, value):
          self.value = value

      # Example of how it would look like with the accept method
      # def accept(self, visitor):
      #     visitor.visit(self)


  class AdditionExpression:
      def __init__(self, left, right):
          self.left = left
          self.right = right


  class ExpressionPrinter:
      def __init__(self):
          self.buffer = []

      @visitor(DoubleExpression)
      def visit(self, de):
          self.buffer.append(str(de.value))

      @visitor(AdditionExpression)
      def visit(self, ae):
          self.buffer.append("(")
          self.visit(ae.left)
          self.buffer.append("+")
          self.visit(ae.right)
          self.buffer.append(")")

      def __str__(self):
          return "".join(self.buffer)


  class ExpressionEvaluator:  # This is a more Pythonic way of doing it without the accept method and using a decorator
      def __init__(self):
          self.value = None

      @visitor(DoubleExpression)
      def visit(self, de):
          self.value = de.value

      @visitor(AdditionExpression)
      def visit(self, ae):
          # ae.left.accept(self) # This is how it would look like with the original visitor pattern
          self.visit(ae.left)  # Without accept we're going to call the method directly
          temp = self.value
          # ae.right.accept(self)
          self.visit(ae.right)
          self.value += temp


  # represents 1+(2+3)
  e = AdditionExpression(
      DoubleExpression(1), AdditionExpression(DoubleExpression(2), DoubleExpression(3))
  )
  printer = ExpressionPrinter()
  printer.visit(e)  # (1+(2+3))

  evaluator = ExpressionEvaluator()
  evaluator.visit(e)  # 6

  print(f"{printer} = {evaluator.value}")  # (1+(2+3)) = 6
  ```
