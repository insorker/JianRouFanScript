from __future__ import annotations
import frontend.ast as Ast


class Symbol:
  def __init__(self, name: str, type: str) -> None:
    self.name: str = name
    self.type: str = type
  
  def __repr__(self) -> str:
    return "<{class_name}(name='{name}', type='{type}'')>".format(
      class_name=self.__class__.__name__,
      name=self.name,
      type=self.type,
    )


class FnSymbol(Symbol):
  def __init__(self, name: str, type: str, params: list[VarSymbol], block: Ast.FnBlock, symtab: SymbolTable) -> None:
    super().__init__(name, type)
    self.params = params
    self.block = block
    self.symtab = symtab

  def __repr__(self) -> str:
    return "<{class_name}(name='{name}', type='{type}', params={params}')>".format(
      class_name=self.__class__.__name__,
      name=self.name,
      type=self.type,
      params=self.params
    )

class VarSymbol(Symbol):
  def __init__(self, name: str, type: str, const: bool) -> None:
    super().__init__(name, type)
    self.const: bool = const
  
  def __repr__(self) -> str:
    return "<{class_name}(name='{name}', type='{type}', const={const}')>".format(
      class_name=self.__class__.__name__,
      name=self.name,
      type=self.type,
      const=self.const
    )
  

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

  def lookup(self, name: str):
    symtab = self._resolve(name)
    return symtab._symbols[name]