from frontend import *


class NodeVisitor:
  def visit(self, node: Ast.AstNode):
    return getattr(
      self,
      f'visit_{type(node).__name__}',
      self.visit_error
    )(node)
  
  def visit_Program(self, program: Ast.Program):
    self.visit_Block(program)
  
  def visit_Block(self, block: Ast.Block):
    for node in block.body:
      self.visit(node)

  def visit_VarDeclarationStmt(self, stmt: Ast.VarDeclarationStmt):
    pass

  def visit_AssignmentExpr(self, expr: Ast.AssignmentExpr):
    pass

  def visit_BinaryExpr(self, expr: Ast.BinaryExpr):
    pass

  def visit_NumberFactor(self, factor: Ast.NumberFactor):
    pass

  def visit_VarFactor(self, factor: Ast.VarFactor):
    pass

  def visit_NullFactor(self, factor: Ast.NullFactor):
    pass

  def visit_error(self, node: Ast.AstNode):
    raise Exception(f'Method visit_{type(node).__name__} is not defined.')