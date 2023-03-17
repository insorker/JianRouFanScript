from backend.value import *
from frontend import *
from .expression import eval_expr
from typing import cast


def eval_stmt(stmt: Ast.Stmt) -> Value:
  return eval_expr(cast(Ast.Expr, stmt))