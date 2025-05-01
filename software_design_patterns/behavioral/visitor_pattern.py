from shared.lib.visitor import visitor

UNKNOWN_EXPRESSION = "Unknown expression type"


class ValueExpression:
    def __init__(self, value):
        self.value = value


class ModuloExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class DivisionExpression:
    def __init__(self, left, right):
        self.left = left
        self.right = right


class ExpressionPrinter:
    def __init__(self):
        self.buffer = []

    @visitor(ValueExpression)
    def visit(self, expression):
        self.buffer.append(str(expression.value))

    @visitor(ModuloExpression)
    def visit(self, expression):
        self.visit(expression.left)
        self.buffer.append("%")
        self.visit(expression.right)

    @visitor(DivisionExpression)
    def visit(self, expression):
        self.visit(expression.left)
        self.buffer.append("/")
        self.visit(expression.right)

    def __str__(self):
        return "".join(self.buffer)


class ExpressionEvaluator:
    def __init__(self):
        self.result = None

    @visitor(ValueExpression)
    def visit(self, expression):
        self.result = expression.value

    @visitor(ModuloExpression)
    def visit(self, expression):
        self.visit(expression.left)
        temp = self.result
        self.visit(expression.right)
        self.result = temp % self.result

    @visitor(DivisionExpression)
    def visit(self, expression):
        self.visit(expression.left)
        temp = self.result
        self.visit(expression.right)
        self.result = temp / self.result
