from .value import Value
from frontend import *
from .evaluator import *
from .environment import Environment


class Interpreter:
  def __init__(self) -> None:
    self.env = Environment()

  def interpret(self, program: Ast.Program) -> list[Value]:
    result = []

    for stmt in program.body:
      result.append(eval_stmt(stmt, self.env))
    
    return result