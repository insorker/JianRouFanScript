from backend.value import *
from frontend import *
from .expression import eval_expr
from ..environment import Environment
from typing import cast


def eval_stmt(stmt: Ast.Stmt, env: Environment) -> Value:
  if stmt.type == Ast.NodeType.DECLARATION_STMT:
    return eval_declaration_stmt(cast(Ast.DeclarationStmt, stmt), env)
  elif stmt.type == Ast.NodeType.ASSIGNMENT_STMT:
    return eval_assignment_stmt(cast(Ast.AssignmentStmt, stmt), env)
  else:
    return eval_expr(cast(Ast.Expr, stmt), env)

def eval_declaration_stmt(stmt: Ast.DeclarationStmt, env: Environment) -> Value:
  env.declare(stmt.left.symbol, eval_expr(stmt.right, env), False)
  return NullValue()

def eval_assignment_stmt(stmt: Ast.AssignmentStmt, env: Environment) -> Value:
  env.assign(stmt.left.symbol, eval_expr(stmt.right, env))
  return NullValue()