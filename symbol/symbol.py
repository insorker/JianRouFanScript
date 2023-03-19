from enum import Enum, auto
from symbol.builtintype import BuiltinType


class Symbol:
  def __init__(self, name: str, type: BuiltinType) -> None:
    self.name: str = name
    self.type: BuiltinType = type
  
  def __repr__(self) -> str:
    return f'<{self.name}, {self.type.name}'


class BuiltinTypeSymbol(Symbol):
  def __init__(self, name: str, type: BuiltinType) -> None:
    super().__init__(name, type)
  

class VarSymbol(Symbol):
  def __init__(self, name: str, type: BuiltinType, const: bool) -> None:
    super().__init__(name, type)
    self.const: bool = const