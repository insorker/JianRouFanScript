class NumericEval:
  @staticmethod
  def int_eval(le: int, ri: int, op: str) -> int:
    if op == '+': return le + ri
    elif op == '-': return le - ri
    elif op == '*': return le * ri
    elif ri == 0:
      raise Exception('Integer division or modulo by zero.')
    elif op == '/': return le // ri
    elif op == '%': return le % ri
    
    raise Exception(f'Unkonw operator {op}.')
  
  @staticmethod
  def float_eval(le: int | float, ri: int | float, op: str) -> float:
    if op == '+': return le + ri
    elif op == '-': return le - ri
    elif op == '*': return le * ri
    elif ri == 0:
      raise Exception('Integer division or modulo by zero.')
    elif op == '/': return le / ri
    elif op == '%': return le % ri
    
    raise Exception(f'Unkonw operator {op}.')