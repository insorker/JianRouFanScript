from __future__ import annotations
from .value import *


class Environment:
  def __init__(self, enclosing_env: Environment | None = None) -> None:
    self.enclosing_env: Environment | None = enclosing_env
    self.variables: dict[str, Value] = dict()
    self.constants: set[str] = set()

  def __repr__(self) -> str:
    return str(self.variables)

  def _resolve(self, varname: str) -> Environment:
    if varname in self.variables:
      return self
    elif self.enclosing_env == None:
      raise Exception(__file__, f'Cannot find variable: {varname}.')
    else:
      return self.enclosing_env._resolve(varname)

  def declare(self, varname: str, value: Value, const: bool = False):
    if varname in self.variables:
      raise Exception(__file__, f'Cannot redeclare variable: {varname}.')
    
    self.variables[varname] = value
    self.constants.add(varname) if const else None
  
  def assign(self, varname: str, value: Value):
    env = self._resolve(varname)

    if varname in env.constants:
      raise Exception(__file__, f'Cannot assign to constant variable: {varname}.')

    env.variables[varname] = value
  
  def lookup(self, varname: str) -> Value:
    env = self._resolve(varname)
    return env.variables[varname]