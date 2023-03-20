from typing import cast
from frontend.ast import *
from frontend.symbol import VarSymbol, SymbolTable


class SemanticAnalyzer(NodeVisitor):
  def __init__(self) -> None:
    self._symtab = SymbolTable(None)
  
  def visit_Program(self, program: Program) -> Program:
    program.symtab = self._symtab

    for node in program.body:
      self.visit(node)

    return program

  def visit_Block(self, block: Block):
    enclosing_symtab = self._symtab
    self._symtab = SymbolTable(self._symtab)
    block.symtab = self._symtab

    for node in block.body:
      self.visit(node)

    self._symtab = enclosing_symtab

  def visit_VarDeclarationStmt(self, stmt: VarDeclarationStmt):
    if type(stmt.left) == VarFactor:
      var = cast(VarFactor, stmt.left)
      self._symtab.declare(VarSymbol(var.name, var.type, stmt.const))
    else:
      raise Exception(f'Cannot assign to {stmt.left.node_type()} here.')
    
  def visit_AssignmentExpr(self, expr: AssignmentExpr):
    if type(expr.left) == VarFactor:
      self.visit(expr.left)
      self.visit(expr.right)
    else:
      raise Exception(f'Cannot assign to {expr.left.node_type()} here.')

  def visit_BinaryExpr(self, expr: BinaryExpr):
    self.visit(expr.left)
    self.visit(expr.right)

  def visit_VarFactor(self, factor: VarFactor):
    self._symtab.lookup(factor.name)