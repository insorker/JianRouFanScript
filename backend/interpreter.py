from .value import NullValue, NumberValue, Value, ValueType
from frontend import *
from .evaluator import *
from typing import cast


class Interpreter:
  def error(self):
    raise Exception(__file__, 'Interpreter error.')

  def interpret(self, program: Ast.Program) -> list[Value]:
    result = []

    for stmt in program.body:
      result.append(eval_stmt(stmt))
    
    return result

  # def eval_stmt(self, stmt: Ast.Stmt) -> Value:
  #   return self.eval_expr(cast(Ast.Expr, stmt))

  # def eval_expr(self, expr: Ast.Expr) -> Value:
  #   if issubclass(expr.__class__, Ast.Factor):
  #     return self.eval_factor(cast(Ast.Factor, expr))
  #   elif expr.type == Ast.NodeType.BINARY_EXPR:
  #     return self.eval_binary_expr(cast(Ast.BinaryExpr, expr))
    
  #   self.error()

  # def eval_binary_expr(self, binaryExpr: Ast.BinaryExpr) -> Value:
  #   left = self.eval_expr(binaryExpr.left)
  #   right = self.eval_expr(binaryExpr.right)

  #   if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
  #     return self.eval_numeric_binary_expr(
  #       cast(NumberValue, left),
  #       binaryExpr.operator,
  #       cast(NumberValue, right)
  #     )

  #   self.error()
  
  # def eval_numeric_binary_expr(self, left: NumberValue, operator: str, right: NumberValue) -> NumberValue:
  #   result: int = 0

  #   if operator == '+':
  #     result = left.value + right.value
  #   elif operator == '-':
  #     result = left.value - right.value
  #   elif operator == '*':
  #     result = left.value * right.value
  #   elif operator == '/':
  #     result = left.value // right.value
    
  #   return NumberValue(result)

  # def eval_factor(self, factor: Ast.Factor) -> Value:
  #   if factor.type == Ast.NodeType.NUMBER_FACTOR:
  #     return self.eval_number_factor(cast(Ast.NumberFactor, factor))
    
  #   self.error()
    
  # def eval_number_factor(self, numberFactor: Ast.NumberFactor) -> Value:
  #   return NumberValue(numberFactor.value)