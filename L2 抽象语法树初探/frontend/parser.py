from .lexer import Token, TokenType, tokenize
from .ast import BinaryExpr, Expr, Factor, NumberFactor, Program, Stmt


class Parser:
  def __init__(self) -> None:
    pass

  def tk(self) -> Token:
    return self.tokens[0]

  def eat(self) -> Token:
    """
      return current token and move to next token
    """
    return self.tokens.pop(0)
  
  def expect(self, tokentype: TokenType) -> Token:
    if self.tk().type == tokentype:
      return self.eat()

    raise Exception(__file__, 'Token expected ', tokentype.name, ' not found. Get ', self.tk(), ' instead.')

  def parse(self, code: str) -> Program:
    self.tokens = tokenize(code)

    return self.parse_program()
  
  def parse_program(self) -> Program:
    """
      Program -> Stmt*
    """
    program = Program()

    while self.tk().type != TokenType.EOF:
      program.body.append(self.parse_stmt())
    
    return program
  
  def parse_stmt(self) -> Stmt:
    """
      Stmt -> Expr
    """
    return self.parse_expr()
  
  def parse_expr(self) -> Expr:
    """
      Expr -> AdditiveExpr
    """
    return self.parse_additive_expr()
  
  def parse_additive_expr(self) -> Expr:
    """
      AdditiveExpr -> MultiplicativeExpr (( PLUS | MINUS ) MultiplicativeExpr)*
    """
    left = self.parse_multiplicative_expr()

    while self.tk().value == '+' or self.tk().value == '-':
      operator = self.eat().value
      right = self.parse_multiplicative_expr()
      left = BinaryExpr(left, operator, right)

    return left

  def parse_multiplicative_expr(self) -> Expr:
    """
      MultiplicativeExpr -> Factor (( MUL | DIV ) Factor)*
    """
    left = self.parse_factor()

    while self.tk().value == '*' or self.tk().value == '/':
      operator = self.eat().value
      right = self.parse_factor()
      left = BinaryExpr(left, operator, right)

    return left
  
  def parse_factor(self) -> Expr:
    """
      Factor -> INTEGER
              | OPEN_PAREN expr CLOSE_PAREN
    """
    if self.tk().type == TokenType.NUMBER:
      return NumberFactor(int(self.eat().value))
    elif self.tk().type == TokenType.OPEN_PAREN:
      self.eat()
      value = self.parse_expr()
      self.expect(TokenType.CLOSE_PAREN)
      return value
    
    raise Exception(__file__, 'Cannot not parse current token.', self.tk())