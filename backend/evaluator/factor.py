from backend.value import *
from frontend import *
from .error import eval_error
from typing import cast


def eval_factor(factor: Ast.Factor) -> Value:
  if factor.type == Ast.NodeType.NUMBER_FACTOR:
    return eval_number_factor(cast(Ast.NumberFactor, factor))
  
  eval_error('Unknow factor.')
  
def eval_number_factor(numberFactor: Ast.NumberFactor) -> Value:
  return NumberValue(numberFactor.value)