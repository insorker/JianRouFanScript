from __future__ import annotations
from enum import Enum, auto
from common.value import Value


class ARType(Enum):
  PROGRAM = auto()
  BLOCK = auto()
  FUNCTION = auto()


class ActivationRecord:
  def __init__(self, name: str, type: ARType, control_link: ActivationRecord | None=None) -> None:
    self.name: str = name
    self.type: ARType = type
    self._control_link: ActivationRecord | None = control_link
    self._locals: dict[str, Value] = {}

  def __repr__(self) -> str:
    return str(self._locals)

  def _resolve(self, name: str) -> ActivationRecord:
    if name in self._locals:
      return self
    elif self._control_link:
      return self._control_link._resolve(name)
    
    raise Exception(f"Runtime error.")
    
  def declare(self, name: str, value: Value):
    self._locals[name] = value
  
  def assign(self, name: str, value: Value):
    ar = self._resolve(name)
    ar._locals[name] = value

  def lookup(self, name: str) -> Value:
    ar = self._resolve(name)
    return ar._locals[name]