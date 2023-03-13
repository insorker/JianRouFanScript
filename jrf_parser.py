from jrf_lexer import Token, TokenType, tokenize
from jrf_ast import AstType, Expr, NumberExpr, Program, Stmt

class Paser:
  def __init__(self) -> None:
    self.tokens: list[Token]
    self.program: Program

  def token(self) -> Token:
    return self.tokens[0]

  def parse(self, srcCode: str) -> Program:
    self.tokens = tokenize(srcCode)
    self.program = Program()

    while self.token().type != TokenType.EOF:
      self.program.body.append(self.parse_stmt())

    return self.program
  
  def parse_stmt(self) -> Stmt:
    return self.parse_expr()

  def parse_expr(self) -> Expr:
    return self.parse_primary_expr()

  def parse_primary_expr(self) -> Expr:
    type = self.token().type

    if type == TokenType.NUMBER:
      return NumberExpr(self.token().value)
