from enum import Enum, auto


class NodeType(Enum):
  PROGRAM = auto()
  
  STMT = auto()
  EXPR = auto()
  FACTOR = auto()

  BINARY_EXPR = auto()
  NUMBER_FACTOR = auto()

class Program:
  def __init__(self) -> None:
    self.type: NodeType = NodeType.PROGRAM
    self.body: list[Stmt] = []

  def __repr__(self) -> str:
    res = '{'
    res += '\n\t' + self.type.name
    for stmt in self.body:
      res += '\n' + stmt.__repr__(1)
    res += '\n}'

    return res

class Stmt:
  def __init__(self) -> None:
    self.type: NodeType = NodeType.STMT

  def __repr__(self, indent) -> str:
    res = indent * '\t' + self.type.name
    return res

class Expr(Stmt):
  def __init__(self) -> None:
    self.type: NodeType = NodeType.EXPR
  
  def __repr__(self, indent) -> str:
    res = indent * '\t' + self.type.name
    return res

class BinaryExpr(Expr):
  def __init__(self, left: Expr, operator: str, right: Expr) -> None:
    self.type: NodeType = NodeType.BINARY_EXPR
    self.left: Expr = left
    self.operator: str = operator
    self.right: Expr = right

  def __repr__(self, indent) -> str:
    res = indent * '\t' + '{'
    res += '\n' + (indent + 1) * '\t' + self.type.name
    res += '\n' + self.left.__repr__(indent + 1)
    res += '\n' + (indent + 1) * '\t' + self.operator
    res += '\n' + self.right.__repr__(indent + 1)
    res += '\n' + indent * '\t' + '}'

    return res

class Factor(Expr):
  def __init__(self) -> None:
    self.type: NodeType = NodeType.FACTOR

class NumberFactor(Factor):
  def __init__(self, value: int) -> None:
    self.type: NodeType = NodeType.NUMBER_FACTOR
    self.value: int = value

  def __repr__(self, indent) -> str:
    return indent * '\t' + f'{{ {self.type.name}, {self.value} }}'