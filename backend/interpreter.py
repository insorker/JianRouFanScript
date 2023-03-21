from typing import cast
from frontend import *
from common.value import *
from backend.activationrecord import *
from backend.evaluator import *


class Interpreter(Ast.NodeVisitor):
  def __init__(self) -> None:
    self._ar: ActivationRecord

  def interpret(self, program: Ast.Program) -> Value | None:
    return self.visit(program)
  
  def visit_Program(self, program: Ast.Program):
    self.ar = ActivationRecord('program', ARType.PROGRAM)

    res: Value = Value()
    for node in program.body:
      res = self.visit(node)

    return res
  
  def visit_Block(self, block: Ast.Block):
    enclosing_ar = self._ar
    self._ar = ActivationRecord('block', ARType.PROGRAM, enclosing_ar)

    for node in block.body:
      self.visit(node)

    self._ar = enclosing_ar

  def visit_VarDeclarationStmt(self, stmt: Ast.VarDeclarationStmt):
    if type(stmt.left) == Ast.VarFactor:
      var = cast(Ast.VarFactor, stmt.left)
      value = self.visit(stmt.right)
      self._ar.set(var.name, value)
    else:
      raise Exception(f'Runtime')

  def visit_AssignmentExpr(self, expr: Ast.AssignmentExpr) -> Value:
    if type(expr.left) == Ast.VarFactor:
      var = cast(Ast.VarFactor, expr.left)
      value = self.visit(expr.right)
      self._ar.set(var.name, value)
      return value
    else:
      raise Exception(f'Runtime')

  def visit_BinaryExpr(self, expr: Ast.BinaryExpr) -> Value:
    left = self.visit(expr.left)
    right = self.visit(expr.right)

    if left.__class__ == Integer and right.__class__ == Integer:
      return Integer(NumericEval.int_eval(left.value, right.value, expr.operator))
    elif Value.isdigit(left) and Value.isdigit(right):
      return Float(NumericEval.float_eval(left.value, right.value, expr.operator))
    
    raise Exception(f'Runtime')

  def visit_IntegerFactor(self, factor: Ast.IntegerFactor) -> Integer:
    return factor.value
  
  def visit_FloatFactor(self, factor: Ast.FloatFactor) -> Float:
    return factor.value

  def visit_VarFactor(self, factor: Ast.VarFactor):
    var = self._ar.get(factor.name)
    return var.value

  def visit_NullFactor(self, factor: Ast.NullFactor):
    pass