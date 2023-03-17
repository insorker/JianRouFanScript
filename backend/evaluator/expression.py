from backend.value import *
from frontend import *
from .factor import eval_error, eval_factor
from ..environment import Environment
from typing import cast


def eval_expr(expr: Ast.Expr, env: Environment) -> Value:
  if issubclass(expr.__class__, Ast.Factor):
    return eval_factor(cast(Ast.Factor, expr), env)
  elif expr.type == Ast.NodeType.BINARY_EXPR:
    return eval_binary_expr(cast(Ast.BinaryExpr, expr), env)
  
  eval_error('Unknow expression.')

def eval_binary_expr( binaryExpr: Ast.BinaryExpr, env: Environment) -> Value:
  left = eval_expr(binaryExpr.left, env)
  right = eval_expr(binaryExpr.right, env)

  if left.type == ValueType.NUMBER and right.type == ValueType.NUMBER:
    return eval_numeric_binary_expr(
      cast(NumberValue, left),
      binaryExpr.operator,
      cast(NumberValue, right)
    )

  eval_error('Unknow binary expression.')

def eval_numeric_binary_expr(left: NumberValue, operator: str, right: NumberValue) -> NumberValue:
  result: int = 0

  if operator == '+':
    result = left.value + right.value
  elif operator == '-':
    result = left.value - right.value
  elif operator == '*':
    result = left.value * right.value
  elif operator == '/':
    result = left.value // right.value
  
  return NumberValue(result)