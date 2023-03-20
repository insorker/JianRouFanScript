from typing import cast
from frontend import *
from common.symbol import SymbolTable, VarSymbol
from common.value import *
from backend.evaluator import *


class Interpreter(Ast.NodeVisitor):
  def __init__(self) -> None:
    self._symtab = SymbolTable(None)

  def interpret(self, program: Ast.Program) -> Value | None:
    return self.visit(program)
  
  def visit_Program(self, program: Ast.Program):
    res = Value()
    for node in program.body:
      res = self.visit(node)

    return res
  
  def visit_Block(self, block: Ast.Block):
    enclosing_symtab = self._symtab
    self._symtab = SymbolTable(enclosing_symtab)

    for node in block.body:
      self.visit(node)

    self._symtab = enclosing_symtab

  def visit_VarDeclarationStmt(self, stmt: Ast.VarDeclarationStmt):
    if type(stmt.left) == Ast.VarFactor:
      var = cast(Ast.VarFactor, stmt.left)
      value = self.visit(stmt.right)
      self._symtab.declare(VarSymbol(var.name, var.type, value, stmt.const))
    else:
      raise Exception(f'Cannot assign to {stmt.left.node_type()} here.')

  def visit_AssignmentExpr(self, expr: Ast.AssignmentExpr) -> Value:
    if type(expr.left) == Ast.VarFactor:
      var = cast(Ast.VarFactor, expr.left)
      value = self.visit(expr.right)
      self._symtab.assign(var.name, value)
      return value
    else:
      raise Exception(f'Cannot assign to {expr.left.node_type()} here.')

  def visit_BinaryExpr(self, expr: Ast.BinaryExpr) -> Value:
    left = self.visit(expr.left)
    right = self.visit(expr.right)

    if left.__class__ == Integer and right.__class__ == Integer:
      return Integer(NumericEval.int_eval(left.value, right.value, expr.operator))
    elif Value.isdigit(left) and Value.isdigit(right):
      return Float(NumericEval.float_eval(left.value, right.value, expr.operator))
    
    raise Exception(f'Invalid binary expr {left} {expr.operator} {right}.')

  def visit_IntegerFactor(self, factor: Ast.IntegerFactor) -> Integer:
    return factor.value
  
  def visit_FloatFactor(self, factor: Ast.FloatFactor) -> Float:
    return factor.value

  def visit_VarFactor(self, factor: Ast.VarFactor):
    var = self._symtab.lookup(factor.name)
    return var.value

  def visit_NullFactor(self, factor: Ast.NullFactor):
    pass