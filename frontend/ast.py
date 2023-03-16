from enum import Enum, auto


class NodeType(Enum):
  PROGRAM = auto()
  # statement
  STMT = auto()
  # expression
  EXPR = auto()
  BINARY_EXPR = auto()
  # factor
  FACTOR = auto()
  NUMBER_FACTOR= auto()

class Program:
  def __init__(self) -> None:
    self.type = NodeType.PROGRAM
    self.body: list[Stmt] = []
  
  def __repr__(self) -> str:
    res = '{'
    res += '\n\t' + self.type.name + ','
    for stmt in self.body:
      res += '\n' + stmt.__repr__(1)
    res += '\n}'
    return res

class Stmt:
  def __init__(self) -> None:
    self.type = NodeType.STMT
  
  def __repr__(self, depth) -> str:
    return '\t' * depth + f'{self.type.name}'
  
class Expr(Stmt):
  def __init__(self) -> None:
    self.type = NodeType.EXPR

class BinaryExpr(Expr):
  def __init__(self, left: Expr, right: Expr, operator: str) -> None:
    self.type = NodeType.BINARY_EXPR
    self.left: Expr = left
    self.right: Expr = right
    self.operator: str = operator
  
  def __repr__(self, depth) -> str:
    res = depth * '\t' + '{'
    res += '\n' + (depth + 1) * '\t' + self.type.name + ','
    res += '\n' + self.left.__repr__(depth+1) + ','
    res += '\n' + (depth + 1) * '\t' + self.operator + ','
    res += '\n' + self.right.__repr__(depth+1) + ','
    res += '\n' + depth * '\t' + '}'

    return res

class Factor(Expr):
  def __init__(self) -> None:
    self.type = NodeType.FACTOR

class NumberFactor(Factor):
  def __init__(self, value: int) -> None:
    self.type = NodeType.NUMBER_FACTOR
    self.value: int = value
  
  def __repr__(self, depth) -> str:
    return depth * '\t' + f'{{ {self.type.name}, {self.value} }}'
