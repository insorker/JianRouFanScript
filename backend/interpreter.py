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
    self._ar = ActivationRecord('program', ARType.PROGRAM)

    for node in program.body:
      self.visit(node)
  
  def visit_Block(self, block: Ast.Block):
    enclosing_ar = self._ar
    self._ar = ActivationRecord('block', ARType.BLOCK, enclosing_ar)

    for node in block.body:
      self.visit(node)

    self._ar = enclosing_ar

  def visit_FnBlock(self, block: Ast.FnBlock) -> Value:
    enclosing_ar = self._ar
    self._ar = ActivationRecord('block', ARType.BLOCK, enclosing_ar)
    result = Undefined()

    for node in block.body:
      if type(node) == Ast.FnReturnStmt:
        result = self.visit(node)
        break
      else:
        self.visit(node)
    
    self._ar = enclosing_ar
    return result

  def visit_VarDeclarationStmt(self, stmt: Ast.VarDeclarationStmt):
    var = cast(Ast.VarFactor, stmt.left)
    value = self.visit(stmt.right)
    self._ar.declare(var.name, value)
    
  def visit_FnDeclarationStmt(self, stmt: Ast.FnDeclarationStmt):
    params = []
    for param in stmt.params:
      params.append(param.name)
    self._ar.declare(stmt.name, Function(stmt.name, params, stmt.block, self._ar))

  def visit_FnReturnStmt(self, stmt: Ast.FnReturnStmt):
    return self.visit(stmt.value)

  def visit_AssignmentExpr(self, expr: Ast.AssignmentExpr) -> Value:
    var = cast(Ast.VarFactor, expr.left)
    value = self.visit(expr.right)
    self._ar.assign(var.name, value)
    return value

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

  def visit_FnCallFactor(self, factor: Ast.FnCallFactor) -> Value:
    if factor.name == 'print':
      for param in factor.params:
        param_value = self.visit(param)
        print(param_value)
      return Value()
    
    fn_symbol = cast(Function, self._ar.lookup(factor.name))

    enclosing_ar = self._ar
    # read params before replace the ar
    fn_ar = ActivationRecord(fn_symbol.name, ARType.FUNCTION, fn_symbol.ar)
    for idx, param in enumerate(factor.params):
      param_name = fn_symbol.params[idx]
      param_value = self.visit(param)
      fn_ar.declare(param_name, param_value)

    self._ar = fn_ar
    value = self.visit(fn_symbol.block)
    self._ar = enclosing_ar
    return value

  def visit_VarFactor(self, factor: Ast.VarFactor):
    return self._ar.lookup(factor.name)