from enum import Enum, auto


class NodeType(Enum):
  # BLOCK
  BLOCK = auto()
  PROGRAM = auto()
  # statement
  STMT = auto()
  VARIABLE_DECLARATION_STMT = auto()
  # expression
  EXPR = auto()
  ASSIGNMENT_EXPR = auto()
  BINARY_EXPR = auto()
  # factor
  FACTOR = auto()
  NUMBER_FACTOR = auto()
  VARIABLE_FACTOR = auto()
  NULL_FACTOR = auto()

class Block:
  def __init__(self) -> None:
    self.type = NodeType.BLOCK
    self.body: list = []

  def __repr__(self, indent) -> str:
    res = indent * '\t' + '{'
    res += '\n' + (indent + 1) * '\t' + self.type.name + ','
    for stmt in self.body:
      res += '\n' + stmt.__repr__(indent + 1)
    res += '\n' + indent * '\t' + '}'
    return res

class Program(Block):
  def __init__(self) -> None:
    self.type = NodeType.PROGRAM
    self.body: list = []
  
  def __repr__(self) -> str:
    res = '{'
    res += '\n' + '\t' + self.type.name + ','
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

class Factor(Expr):
  def __init__(self) -> None:
    self.type = NodeType.FACTOR

class VariableDeclarationStmt(Stmt):
  def __init__(self, left: Expr, right: Expr, const: bool) -> None:
    self.type = NodeType.VARIABLE_DECLARATION_STMT
    self.left: Expr = left
    self.right: Expr = right
    self.const: bool = const

class AssignmentExpr(Expr):
  def __init__(self, left: Expr, right: Expr) -> None:
    self.type = NodeType.ASSIGNMENT_EXPR
    self.left: Expr = left
    self.right: Expr = right

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

class NumberFactor(Factor):
  def __init__(self, value: int) -> None:
    self.type = NodeType.NUMBER_FACTOR
    self.value: int = value
  
  def __repr__(self, depth) -> str:
    return depth * '\t' + f'{{ {self.type.name}, {self.value} }}'

class VariableFactor(Factor):
  def __init__(self, symbol: str) -> None:
    self.type = NodeType.VARIABLE_FACTOR
    self.symbol: str = symbol
  
  def __repr__(self, depth) -> str:
    return depth * '\t' + f'{{ {self.type.name}, {self.symbol} }}'

class NullFactor(Factor):
  def __init__(self) -> None:
    self.type = NodeType.NULL_FACTOR
  
  def __repr__(self, depth) -> str:
    return depth * '\t' + f'{{ {self.type.name} }}'