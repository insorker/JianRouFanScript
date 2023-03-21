from typing import cast
from frontend.ast import *
from frontend.symbol import *
from common.error import SemanticError


class SemanticAnalyzer(NodeVisitor):
  def __init__(self) -> None:
    self._symtab: SymbolTable
  
  def visit_Program(self, program: Program):
    self._symtab = SymbolTable(None)

    for node in program.body:
      self.visit(node)

  def visit_Block(self, block: Block):
    enclosing_symtab = self._symtab
    self._symtab = SymbolTable(self._symtab)

    for node in block.body:
      if self.visit(node):
        raise SemanticError(f'\'return\' outside function')

    self._symtab = enclosing_symtab

  def visit_FnBlock(self, block: FnBlock):
    enclosing_symtab = self._symtab
    self._symtab = SymbolTable(self._symtab)

    for node in block.body:
      if self.visit(node):
        break

    self._symtab = enclosing_symtab

  def visit_VarDeclarationStmt(self, stmt: VarDeclarationStmt):
    if type(stmt.left) == VarFactor:
      var = cast(VarFactor, stmt.left)
      self._symtab.declare(VarSymbol(var.name, var.type, stmt.const))
    else:
      raise SemanticError(f'Cannot assign to {stmt.left.node_type()} here.')
    
  def visit_FnDeclarationStmt(self, stmt: FnDeclarationStmt):
    params = []
    for param in stmt.params:
      params.append(self.visit(param))
    self._symtab.declare(FnSymbol(stmt.name, stmt.type, params, stmt.block, self._symtab))

  def visit_FnReturnStmt(self, stmt: FnReturnStmt):
    self.visit(stmt.value)
    return True
    
  def visit_AssignmentExpr(self, expr: AssignmentExpr):
    if type(expr.left) == VarFactor:
      symbol = self.visit(expr.left)
      if symbol.const:
        raise SemanticError(f'Cannot assign to {symbol} because it is a constant.')
      self.visit(expr.right)
    else:
      raise SemanticError(f'Cannot assign to {expr.left.node_type()} here.')

  def visit_BinaryExpr(self, expr: BinaryExpr):
    self.visit(expr.left)
    self.visit(expr.right)

  def visit_FnCallFactor(self, factor: FnCallFactor):
    symbol = self._symtab.lookup(factor.name)
    if type(symbol) == FnSymbol:
      symbol = cast(FnSymbol, symbol)
    else:
      raise SemanticError(f'\'{factor}\' is not callable.')
    enclosing_symtab = self._symtab
    self._symtab = SymbolTable(symbol.symtab)

    if len(symbol.params) == len(factor.params):
      for idx, param in enumerate(factor.params):
        var = cast(VarFactor, param)
        self._symtab.declare(VarSymbol(var.name, var.type, False))
      self.visit(symbol.block)
    else:
      raise SemanticError(f'{symbol} takes {len(symbol.params)} positional arguments but {len(factor.params)} was given.')
    
    self._symtab = enclosing_symtab

  def visit_VarFactor(self, factor: VarFactor) -> Symbol:
    return self._symtab.lookup(factor.name)