from __future__ import annotations
from common.value import *


class AstNode:
  """abstract class"""
  def node_type(self) -> str:
    """return class name"""
    return self.__class__.__name__

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
  """abstract class"""
  pass


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
  

class FunctionStmt(AstNode):
  def __init__(self, name: str, params: list[VarFactor], block: Block) -> None:
    super().__init__()
    self.name = name
    self.params = params
    self.block = block

  def __repr__(self, indent: int) -> str:
    res = f'{self._tab(indent)}{{'
    res += f'\n{self._tab(indent+1)}{self.node_type()},'
    res += f'\n{self._tab(indent+1)}name: {self.name},'
    res += f'\n{self._tab(indent+1)}'
    for param in self.params:
      res += f'\n{param.__repr__(indent+1)},'
    res += f'\n{self.block.__repr__(indent+1)},'
    return res


class Expr(Stmt):
  """abstract class"""
  pass


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


class Factor(Expr):
  """abstract class"""
  def __init__(self, type: str) -> None:
    super().__init__()
    self.type: str = type


class IntegerFactor(Factor):
  def __init__(self, value: Integer) -> None:
    super().__init__(Integer.__name__)
    self.value: Integer = value
  
  def __repr__(self, indent) -> str:
    return f'{self._tab(indent)}{{ {self.node_type()}, {self.value} }}'
  

class FloatFactor(Factor):
  def __init__(self, value: Float) -> None:
    super().__init__(Float.__name__)
    self.value: Float = value
  
  def __repr__(self, indent) -> str:
    return f'{self._tab(indent)}{{ {self.node_type()}, {self.value} }}'


class VarFactor(Factor):
  def __init__(self, type: str, name: str) -> None:
    super().__init__(type)
    self.name: str = name
  
  def __repr__(self, indent) -> str:
    return f'{self._tab(indent)}{{ {self.node_type()}, {self.name} }}'


class UndefinedFactor(Factor):
  def __init__(self) -> None:
    super().__init__(Null.__name__)
    self.value: Undefined = Undefined()


class NullFactor(Factor):
  def __init__(self) -> None:
    super().__init__(Null.__name__)
    self.value: Null = Null()
  

class NodeVisitor:
  def visit(self, node: AstNode):
    return getattr(
      self,
      f'visit_{type(node).__name__}',
      self.visit_error
    )(node)
  
  def visit_Program(self, program: Program):
    self.visit_Block(program)
  
  def visit_Block(self, block: Block):
    for node in block.body:
      self.visit(node)

  def visit_VarDeclarationStmt(self, stmt: VarDeclarationStmt):
    pass

  def visit_AssignmentExpr(self, expr: AssignmentExpr):
    pass

  def visit_BinaryExpr(self, expr: BinaryExpr):
    pass

  def visit_IntegerFactor(self, factor: IntegerFactor):
    pass

  def visit_FloatFactor(self, factor: FloatFactor):
    pass

  def visit_VarFactor(self, factor: VarFactor):
    pass

  def visit_NullFactor(self, factor: NullFactor):
    pass

  def visit_error(self, node: AstNode):
    raise Exception(f'Method visit_{type(node).__name__} is not defined.')