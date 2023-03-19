from typing import Union
from symbol.builtintype import BuiltinType


class AstNode:
  def node_type(self) -> str:
    """return class name"""
    return type(self).__name__

  def _tab(self, level: int) -> str:
    return '  ' * level

  def __repr__(self, indent: int) -> str:
    return f'{self._tab(indent)}{{ {self.node_type()} }}'


class Block(AstNode):
  def __init__(self) -> None:
    self.body: list = []

  def __repr__(self, indent: int) -> str:
    res = f'{self._tab(indent)}{{'
    res += f'\n{self._tab(indent+1)}{self.node_type()},'
    res += f'\n{chr(10).join([stmt.__repr__(indent+1) for stmt in self.body])}'
    res += f'\n{self._tab(indent)}}}'
    return res


class Program(Block):
  def __init__(self) -> None:
    self.body: list = []
  
  def __repr__(self) -> str:
    return super().__repr__(0)


class Stmt(AstNode):
  pass


class Expr(Stmt):
  pass


class Factor(Expr):
  def __init__(self, type: BuiltinType) -> None:
    self.type: BuiltinType = type


class VarDeclarationStmt(Stmt):
  def __init__(self, left: Expr, right: Expr, const: bool) -> None:
    self.left: Expr = left
    self.right: Expr = right
    self.const: bool = const

  def __repr__(self, indent: int) -> str:
    res = f'{self._tab(indent)}{{'
    res += f'\n{self._tab(indent+1)}{self.node_type()},'
    res += f'\n{self.left.__repr__(indent+1)},'
    res += f'\n{self.right.__repr__(indent+1)},'
    res += f'\n{self._tab(indent+1)}{{ const: {self.const} }},'
    res += f'\n{self._tab(indent)}}}'
    return res


class AssignmentExpr(Expr):
  def __init__(self, left: Expr, right: Expr) -> None:
    self.left: Expr = left
    self.right: Expr = right
  
  def __repr__(self, indent: int) -> str:
    res = f'{self._tab(indent)}{{'
    res += f'\n{self._tab(indent+1)}{self.node_type()},'
    res += f'\n{self.left.__repr__(indent+1)},'
    res += f'\n{self.right.__repr__(indent+1)},'
    res += f'\n{self._tab(indent)}}}'
    return res


class BinaryExpr(Expr):
  def __init__(self, left: Expr, right: Expr, operator: str) -> None:
    self.left: Expr = left
    self.right: Expr = right
    self.operator: str = operator
  
  def __repr__(self, indent) -> str:
    res = f'{self._tab(indent)}{{'
    res += f'\n{self._tab(indent+1)}{self.node_type()},'
    res += f'\n{self.left.__repr__(indent+1)},'
    res += f'\n{self._tab(indent+1)}{{ operator: {self.operator} }},'
    res += f'\n{self.right.__repr__(indent+1)},'
    res += f'\n{self._tab(indent)}}}'
    return res


class NumberFactor(Factor):
  def __init__(self, type: BuiltinType, value: Union[int, float]) -> None:
    super().__init__(type)
    self.value: Union[int, float] = value
  
  def __repr__(self, indent) -> str:
    return f'{self._tab(indent)}{{ {self.node_type()}, {self.value} }}'


class VarFactor(Factor):
  def __init__(self, type: BuiltinType, name: str) -> None:
    super().__init__(type)
    self.name: str = name
  
  def __repr__(self, indent) -> str:
    return f'{self._tab(indent)}{{ {self.node_type()}, {self.name} }}'


class NullFactor(Factor):
  def __init__(self) -> None:
    super().__init__(BuiltinType.NULL)
  
  def __repr__(self, indent) -> str:
    return f'{self._tab(indent)}{{ {self.node_type()} }}'