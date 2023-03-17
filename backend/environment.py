from .value import *


class SymbolTable:
  def __init__(self) -> None:
    self.variables: dict[str, Value] = dict()
    self.constants: set[str] = set()

  def declare(self, varname: str, value: Value, const: bool):
    if varname in self.variables:
      raise Exception(__file__, f'Cannot redeclare variable: {varname}')
    
    self.variables[varname] = value
    if const:
      self.constants.add(varname)
  
  def assign(self, varname: str, value: Value) -> bool:
    if varname in self.constants:
      raise Exception(__file__, f'Cannot assign to constant variable: {varname}')
    
    if varname not in self.variables:
      return False
    else:
      self.variables[varname] = value
      return True
  
  def has_variable(self, varname: str) -> bool:
    return varname in self.variables
  
  def get_value(self, varname: str) -> Value:
    return self.variables[varname]
    
class Environment:
  def __init__(self) -> None:
    self.stack: list[SymbolTable] = [SymbolTable()]

  def at(self) -> SymbolTable:
    return self.stack[-1]

  def push(self):
    self.stack.append(SymbolTable())
  
  def pop(self):
    self.stack.pop()

  def get_symbol_table(self, varname: str) -> SymbolTable:
    for symboltable in self.stack[::-1]:
      if symboltable.has_variable(varname):
        return symboltable
    
    raise Exception(__file__, f'Cannot find variable: {varname}')
  
  def declare(self, varname: str, value: Value, const: bool):
    self.at().declare(varname, value, const)
  
  def assign(self, varname: str, value: Value):
    self.get_symbol_table(varname).assign(varname, value)

  def get_value(self, varname: str) -> Value:
    return self.get_symbol_table(varname).get_value(varname)