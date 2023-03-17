from enum import Enum, auto


class ValueType(Enum):
  NUMBER = auto()
  NULL = auto()

class Value:
  def __init__(self, type: ValueType) -> None:
    self.type: ValueType = type
    self.value: str = ''
  
  def __repr__(self) -> str:
    return str(self.value)

class NumberValue(Value):
  def __init__(self, value: int) -> None:
    super().__init__(ValueType.NUMBER)
    self.value: int = value

class NullValue(Value):
  def __init__(self) -> None:
    super().__init__(ValueType.NULL)
    self.value: str = 'null'