from __future__ import annotations
from visitor.visitor import NodeVisitor
from symbol.symbol import Symbol, VarSymbol
from frontend import *
from typing import cast


class SymbolTable(NodeVisitor):
  def __init__(self, enclosing_symtab: SymbolTable | None) -> None:
    self._enclosing_symtab: SymbolTable | None = enclosing_symtab
    self._symbols: dict[str, Symbol] = dict()

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
  

class SymbolTableBuilder(NodeVisitor):
  def __init__(self) -> None:
    self._symtab = SymbolTable(None)
  
  def visit_Program(self, program: Ast.Program):
    for node in program.body:
      self.visit(node)

  def visit_Block(self, block: Ast.Block):
    enclosing_symtab = self._symtab
    self._symtab = SymbolTable(self._symtab)

    for node in block.body:
      self.visit(node)

    self._symtab = enclosing_symtab

  def visit_VarDeclarationStmt(self, stmt: Ast.VarDeclarationStmt):
    if type(stmt.left) == Ast.VarFactor:
      var = cast(Ast.VarFactor, stmt.left)
      self._symtab.declare(VarSymbol(var.name, var.type, stmt.const))
    
    raise Exception(f'Cannot assign to {stmt.left.node_type()}.')