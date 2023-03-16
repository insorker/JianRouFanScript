from backend.value import NullValue, Value
from frontend import *



class Interpreter:
  def interpret(self, program: Ast.Program) -> list[Value]:
    result = []

    for stmt in program.body:
      result.append(self.eval(stmt))
    
    return result

  def eval(self, stmt: Ast.Stmt) -> Value:
    if stmt.type == Ast.NodeType.BINARY_EXPR:
      return self.eval_binary_expr(stmt)
    
    return NullValue()

  def eval_binary_expr(self, binaryExpr: Ast.BinaryExpr) -> Value:
    left = self.eval(binaryExpr.left)
    right = self.eval(binaryExpr.right)

    return left + right