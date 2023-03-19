from frontend import *

from backend.value import NullValue, Value, ValueType, NumberValue
from backend.environment import Environment
from backend.evaluator.factor import eval_error, eval_factor

from typing import cast


def eval_expr(expr: Ast.Expr, env: Environment) -> Value:
  if issubclass(expr.__class__, Ast.Factor):
    return eval_factor(cast(Ast.Factor, expr), env)
  elif expr.type == Ast.NodeType.ASSIGNMENT_EXPR:
    return eval_assignment_expr(cast(Ast.AssignmentExpr, expr), env)
  elif expr.type == Ast.NodeType.BINARY_EXPR:
    return eval_binary_expr(cast(Ast.BinaryExpr, expr), env)
  
  eval_error('Unknow expression.')

def eval_assignment_expr(stmt: Ast.AssignmentExpr, env: Environment) -> Value:
  if stmt.left.type == Ast.NodeType.VARIABLE_FACTOR:
    varname = cast(Ast.VariableFactor, stmt.left).symbol
    value = eval_expr(stmt.right, env)

    env.assign(varname, value)
    return value
  
  return NullValue()

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