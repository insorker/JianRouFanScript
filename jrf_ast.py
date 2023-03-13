from enum import Enum, auto
from typing import Union

class AstType(Enum):
  # statement
  PROGRAM = auto(),

  # expression
  NUMBER = auto(),
  IDENTIFIER = auto(),
  BINARY_EXPR = auto(),

# statement
class Stmt:
  def __init__(self, type: AstType) -> None:
    self.type: AstType = type

class Program(Stmt):
  def __init__(self) -> None:
    super().__init__(AstType.PROGRAM)
    self.body: list[Stmt] = []

# expression
class Expr(Stmt):
  def __init__(self, type: AstType) -> None:
    super().__init__(AstType.PROGRAM)

class BinaryExpr(Expr):
  def __init__(self, left: Expr, right: Expr, op: str) -> None:
    super().__init__(AstType.BINARY_EXPR)
    self.left: Expr = left
    self.right: Expr = right
    self.operator: str = op

class NumberExpr(Expr):
  def __init__(self, value: Union[int, float]) -> None:
    super().__init__(AstType.NUMBER)
    self.value: Union[int, float] = value

class IdentifierExpr(Expr):
  def __init__(self, value: str) -> None:
    super().__init__(AstType.IDENTIFIER)
    self.value: str = value