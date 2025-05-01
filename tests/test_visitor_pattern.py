from software_design_patterns.behavioral.visitor_pattern import *


def test_visitor_modulo():
    # 5 % 2 % 3
    expr = ModuloExpression(
        ModuloExpression(ValueExpression(5), ValueExpression(2)), ValueExpression(3)
    )

    printer = ExpressionPrinter()
    printer.visit(expr)
    assert str(printer) == "5%2%3"

    evaluator = ExpressionEvaluator()
    evaluator.visit(expr)
    assert evaluator.result == 5 % 2 % 3


def test_visitor_division():
    # 5 / 2 / 3
    expr = DivisionExpression(
        DivisionExpression(ValueExpression(5), ValueExpression(2)), ValueExpression(3)
    )

    printer = ExpressionPrinter()
    printer.visit(expr)
    assert str(printer) == "5/2/3"

    evaluator = ExpressionEvaluator()
    evaluator.visit(expr)
    assert evaluator.result == 5 / 2 / 3


def test_visitor_modulo_division():
    # 5 % 2 / 3
    expr = DivisionExpression(
        ModuloExpression(ValueExpression(5), ValueExpression(2)), ValueExpression(3)
    )

    printer = ExpressionPrinter()
    printer.visit(expr)
    assert str(printer) == "5%2/3"

    evaluator = ExpressionEvaluator()
    evaluator.visit(expr)
    assert evaluator.result == 5 % 2 / 3
