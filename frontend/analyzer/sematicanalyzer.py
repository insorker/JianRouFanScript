from typing import cast
from frontend.ast import NodeVisitor
from frontend.symbol import VarSymbol, SymbolTable
from frontend import *


class SemanticAnalyzer(NodeVisitor):
  def __init__(self) -> None:
    self._symtab = SymbolTable(None)
  
  def visit_Program(self, program: Ast.Program) -> Ast.Program:
    program.symtab = self._symtab

    for node in program.body:
      self.visit(node)

    return program

  def visit_Block(self, block: Ast.Block):
    enclosing_symtab = self._symtab
    self._symtab = SymbolTable(self._symtab)
    block.symtab = self._symtab

    for node in block.body:
      self.visit(node)

    self._symtab = enclosing_symtab

  def visit_VarDeclarationStmt(self, stmt: Ast.VarDeclarationStmt):
    if type(stmt.left) == Ast.VarFactor:
      var = cast(Ast.VarFactor, stmt.left)
      self._symtab.declare(VarSymbol(var.name, var.type, stmt.const))
    else:
      raise Exception(f'Cannot assign to {stmt.left.node_type()} here.')
    
  def visit_AssignmentExpr(self, expr: Ast.AssignmentExpr):
    if type(expr.left) == Ast.VarFactor:
      self.visit(expr.left)
      self.visit(expr.right)
    else:
      raise Exception(f'Cannot assign to {expr.left.node_type()} here.')

  def visit_BinaryExpr(self, expr: Ast.BinaryExpr):
    self.visit(expr.left)
    self.visit(expr.right)

  def visit_VarFactor(self, factor: Ast.VarFactor):
    self._symtab.lookup(factor.name)