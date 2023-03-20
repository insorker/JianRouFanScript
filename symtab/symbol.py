from symtab.builtintype import BuiltinType


class Symbol:
  def __init__(self, name: str, type: BuiltinType) -> None:
    self.name: str = name
    self.type: BuiltinType = type
  
  def __repr__(self) -> str:
    return "<{class_name}(name='{name}', type='{type}')>".format(
      class_name=self.__class__.__name__,
      name=self.name,
      type=self.type,
    )
  

class VarSymbol(Symbol):
  def __init__(self, name: str, type: BuiltinType, const: bool) -> None:
    super().__init__(name, type)
    self.const: bool = const
  
  def __repr__(self) -> str:
    return "<{class_name}(name='{name}', type='{type}', const={const}')>".format(
      class_name=self.__class__.__name__,
      name=self.name,
      type=self.type,
      const=self.const
    )