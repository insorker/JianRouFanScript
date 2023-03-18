from frontend import *

from backend.value import Value
from backend.evaluator import eval_scope
from backend.environment import Environment


class Interpreter:
  def __init__(self) -> None:
    self.env = Environment()

  def interpret(self, program: Ast.Program) -> Value | None:
    return eval_scope(program, self.env)