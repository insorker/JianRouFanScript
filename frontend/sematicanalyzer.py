from typing import cast
from frontend.ast import *
from common.symbol import VarSymbol, SymbolTable
from common.error import SemanticError


class SemanticAnalyzer(NodeVisitor):
  def __init__(self) -> None:
    self._symtab = SymbolTable(None)
  
  def visit_Program(self, program: Program):
    for node in program.body:
      self.visit(node)

  def visit_Block(self, block: Block):
    enclosing_symtab = self._symtab
    self._symtab = SymbolTable(self._symtab)

    for node in block.body:
      self.visit(node)

    self._symtab = enclosing_symtab

  def visit_VarDeclarationStmt(self, stmt: VarDeclarationStmt):
    if type(stmt.left) == VarFactor:
      var = cast(VarFactor, stmt.left)
      self._symtab.declare(VarSymbol(var.name, var.type, Value(), stmt.const))
    else:
      raise SemanticError(f'Cannot assign to {stmt.left.node_type()} here.')
    
  def visit_AssignmentExpr(self, expr: AssignmentExpr):
    if type(expr.left) == VarFactor:
      self.visit(expr.left)
      self.visit(expr.right)
    else:
      raise SemanticError(f'Cannot assign to {expr.left.node_type()} here.')

  def visit_BinaryExpr(self, expr: BinaryExpr):
    self.visit(expr.left)
    self.visit(expr.right)

  def visit_VarFactor(self, factor: VarFactor):
    self._symtab.lookup(factor.name)