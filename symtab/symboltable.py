from __future__ import annotations
from symtab.symbol import Symbol, VarSymbol
from frontend import *


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
      raise Exception(f'Cannot redeclare {symbol.type.name} symbol: {symbol.name}.')

    self._symbols[symbol.name] = symbol

  def assign(self, symbol: Symbol):
    symtab = self._resolve(symbol.name)
    symtab._symbols[symbol.name] = symbol
  
  def lookup(self, name: str):
    symtab = self._resolve(name)
    return symtab._symbols.get(name)