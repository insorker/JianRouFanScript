from .ast import BinaryExpr, Expr, Factor, NumberFactor, Program, Stmt
from .lexer import Token, TokenType, tokenize


class Parser:
  def __init__(self) -> None:
    self.tokens: list[Token] = []

  def tk(self) -> Token:
    """return current token or None in parser"""
    return self.tokens[0]

  def eat(self) -> Token:
    return self.tokens.pop(0)

  def parse(self, code: str) -> Program:
    self.tokens = tokenize(code)

    return self.parse_program()

  def parse_program(self) -> Program:
    program: Program = Program()

    while self.tk().type != TokenType.EOF:
      program.body.append(self.parse_stmt())
    
    return program

  def parse_stmt(self) -> Stmt:
    return self.parse_expr()
  
  def parse_expr(self) -> Expr:
    return self.parse_additive_expr()
  
  def parse_additive_expr(self) -> Expr:
    left = self.parse_multiplicative_expr()

    while self.tk().value == '+' or self.tk().value == '-':
      operator = self.eat().value
      right = self.parse_multiplicative_expr()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_multiplicative_expr(self) -> Expr:
    left = self.parse_factor()

    while self.tk().value == '*' or self.tk().value == '/':
      operator = self.eat().value
      right = self.parse_factor()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_factor(self) -> Factor:
    if self.tk().type == TokenType.NUMBER:
      return NumberFactor(int(self.eat().value))
      

    raise Exception(__file__, 'Cannot parse ', self.tk, ' to factor.')