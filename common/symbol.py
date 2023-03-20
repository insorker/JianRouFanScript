from __future__ import annotations
from common.value import Value


class Symbol:
  def __init__(self, name: str, type: str, value: Value) -> None:
    self.name: str = name
    self.type: str = type
    self.value: Value = value
  
  def __repr__(self) -> str:
    return "<{class_name}(name='{name}', type='{type}', value='{value}')>".format(
      class_name=self.__class__.__name__,
      name=self.name,
      type=self.type,
      value=self.value,
    )
  
  def setValue(self, value: Value):
    self.value = value
  

class VarSymbol(Symbol):
  def __init__(self, name: str, type: str, value: Value, const: bool) -> None:
    super().__init__(name, type, value)
    self.const: bool = const
  
  def __repr__(self) -> str:
    return "<{class_name}(name='{name}', type='{type}', value={value}, const={const}')>".format(
      class_name=self.__class__.__name__,
      name=self.name,
      type=self.type,
      value=self.value,
      const=self.const
    )
  
  def setValue(self, value: Value):
    if not self.const:
      super().setValue(value)
    else:
      raise Exception(f'Cannot assign to {self.name} because it is a constant.')
  

class SymbolTable:
  def __init__(self, enclosing_symtab: SymbolTable | None) -> None:
    self._enclosing_symtab: SymbolTable | None = enclosing_symtab
    self._symbols: dict[str, Symbol] = dict()

  def __repr__(self) -> str:
    header = 'Symbol Table'
    lines = ['\n', header, '-' * len(header)]
    lines.extend(
      ('%8s: %r' % (key, value))
      for key, value in self._symbols.items()
    )
    return '\n'.join(lines) + '\n'
  
  def _resolve(self, name: str) -> SymbolTable:
    if name in self._symbols:
      return self
    elif self._enclosing_symtab:
      return self._enclosing_symtab._resolve(name)
    
    raise Exception(f"Name '{name}' is not defined.")
  
  def declare(self, symbol: Symbol):
    if symbol.name in self._symbols:
      raise Exception(f'Cannot redeclare {symbol.type} symbol: {symbol.name}.')

    self._symbols[symbol.name] = symbol

  def assign(self, name: str, value: Value):
    symtab = self._resolve(name)
    symbol = symtab._symbols[name]
    symbol.setValue(value)
  
  def lookup(self, name: str):
    symtab = self._resolve(name)
    return symtab._symbols[name]