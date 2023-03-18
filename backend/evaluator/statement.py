from frontend import *

from backend.value import Value, NullValue
from backend.environment import Environment
from backend.evaluator.expression import eval_expr

from typing import cast


def eval_block(scope: Ast.Block, env: Environment) -> Value | None:
  result = None

  for stmt in scope.body:
    if type(stmt) == Ast.Block:
      nested_env = Environment(env)
      result = eval_block(stmt, nested_env)
    else:
      result = eval_stmt(stmt, env)

  return result

def eval_stmt(stmt: Ast.Stmt, env: Environment) -> Value:
  if stmt.type == Ast.NodeType.VARIABLE_DECLARATION_STMT:
    return eval_declaration_stmt(cast(Ast.VariableDeclarationStmt, stmt), env)
  elif stmt.type == Ast.NodeType.ASSIGNMENT_STMT:
    return eval_assignment_stmt(cast(Ast.AssignmentStmt, stmt), env)
  else:
    return eval_expr(cast(Ast.Expr, stmt), env)

def eval_declaration_stmt(stmt: Ast.VariableDeclarationStmt, env: Environment) -> Value:
  if stmt.left.type == Ast.NodeType.VARIABLE_FACTOR:
    env.declare(cast(Ast.VariableFactor, stmt.left).symbol, eval_expr(stmt.right, env))
  return NullValue()

def eval_assignment_stmt(stmt: Ast.AssignmentStmt, env: Environment) -> Value:
  if stmt.left.type == Ast.NodeType.VARIABLE_FACTOR:
    env.assign(cast(Ast.VariableFactor, stmt.left).symbol, eval_expr(stmt.right, env))
  return NullValue()