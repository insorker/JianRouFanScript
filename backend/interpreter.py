from frontend import *

from backend.value import Value
from backend.evaluator import eval_block
from backend.environment import Environment


class Interpreter:
  def __init__(self) -> None:
    self.env = Environment()

  def interpret(self, program: Ast.Program) -> Value | None:
    return eval_block(program, self.env)