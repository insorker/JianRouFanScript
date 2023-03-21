from __future__ import annotations


class Value:
  def __init__(self) -> None:
    self.value: str = 'VALUE'
  
  def __repr__(self) -> str:
    return str(self.value)
  
  @staticmethod
  def isdigit(value: Value) -> bool:
    if type(value) == Integer or type(value) == Float:
      return True
    return False
  

class Function(Value):
  def __init__(self, name: str, params: list[str], block, ar) -> None:
    super().__init__()
    self.value = name
    self.name = name
    self.params = params
    self.block = block
    self.ar = ar


class Integer(Value):
  def __init__(self, value: int) -> None:
    super().__init__()
    self.value: int = value


class Float(Value):
  def __init__(self, value: float) -> None:
    super().__init__()
    self.value: float = value


class Any(Value):
  def __init__(self) -> None:
    super().__init__()
    self.value: str = 'any'


class Undefined(Value):
  def __init__(self) -> None:
    super().__init__()
    self.value: str = 'undefined'