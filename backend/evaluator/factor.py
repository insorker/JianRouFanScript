from backend.value import *
from frontend import *
from .error import eval_error
from ..environment import Environment
from typing import cast


def eval_factor(factor: Ast.Factor, env: Environment) -> Value:
  if factor.type == Ast.NodeType.NUMBER_FACTOR:
    return eval_number_factor(cast(Ast.NumberFactor, factor))
  elif factor.type == Ast.NodeType.VARIABLE_FACTOR:
    return eval_variable_factor(cast(Ast.VariableFactor, factor), env)
  elif factor.type == Ast.NodeType.NULL_FACTOR:
    return eval_null_factor(cast(Ast.NullFactor, factor))
  
  eval_error(f'Unknow factor: {factor.type.name}.')
  
def eval_number_factor(numberFactor: Ast.NumberFactor) -> Value:
  return NumberValue(numberFactor.value)

def eval_variable_factor(variableFactor: Ast.VariableFactor, env: Environment) -> Value:
  value = env.lookup(variableFactor.symbol)
  return cast(NumberValue, value)

def eval_null_factor(nullFactor: Ast.NullFactor) -> Value:
  return NullValue()