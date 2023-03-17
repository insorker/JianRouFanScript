from .value import NullValue, NumberValue, Value, ValueType
from frontend import *
from .evaluator import *
from .environment import Environment
from typing import cast


class Interpreter:
  def __init__(self) -> None:
    self.env = Environment()
  def error(self):
    raise Exception(__file__, 'Interpreter error.')

  def interpret(self, program: Ast.Program) -> list[Value]:
    result = []

    for stmt in program.body:
      result.append(eval_stmt(stmt, self.env))
    
    return result