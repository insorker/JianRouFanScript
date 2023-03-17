from .value import Value
from frontend import *
from .evaluator import *
from .environment import Environment


class Interpreter:
  def __init__(self) -> None:
    self.env = Environment()

  def interpret(self, program: Ast.Program) -> Value | None:
    return eval_scope(program.body, self.env)