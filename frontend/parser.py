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
  
  def expect(self, type: TokenType, err: str) -> Token:
    if self.tk().type == type:
      return self.eat()
    raise Exception(__file__ + err)

  def parse(self, code: str) -> Program:
    self.tokens = tokenize(code)

    return self.parse_program()

  def parse_program(self) -> Program:
    """
      program: stmt*
    """
    program: Program = Program()

    while self.tk().type != TokenType.EOF:
      program.body.append(self.parse_stmt())
    
    return program

  def parse_stmt(self) -> Stmt:
    """
      stmt: expr
    """
    return self.parse_expr()
  
  def parse_expr(self) -> Expr:
    """
      expr: additive_expr
    """
    return self.parse_additive_expr()
  
  def parse_additive_expr(self) -> Expr:
    """
      additive_expr: multiplicative_expr ((PLUS | MINUS) multiplicative_expr)*
    """
    left = self.parse_multiplicative_expr()

    while self.tk().value == '+' or self.tk().value == '-':
      operator = self.eat().value
      right = self.parse_multiplicative_expr()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_multiplicative_expr(self) -> Expr:
    """
      multiplicative_expr: factor ((MUL | DIV) factor)*
    """
    left = self.parse_factor()

    while self.tk().value == '*' or self.tk().value == '/':
      operator = self.eat().value
      right = self.parse_factor()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_factor(self) -> Expr:
    """
      factor: NUMBER
            | OPEN_PAREN expr CLOSE_PAREN
    """
    if self.tk().type == TokenType.NUMBER:
      return NumberFactor(int(self.eat().value))
    elif self.tk().type == TokenType.OPEN_PAREN:
      self.eat()
      value = self.parse_expr()
      self.expect(TokenType.CLOSE_PAREN, 'Missing closs parenthesis or unexpected token.')
      return value

    raise Exception(__file__, 'Cannot parse ', self.tk, ' to factor.')