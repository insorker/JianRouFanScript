from typing import cast
from .ast import AssignmentStmt, BinaryExpr, DeclarationStmt, Expr, Factor, VariableFactor, NullFactor, NumberFactor, Program, Stmt
from .lexer import Token, TokenType, tokenize


class Parser:
  def __init__(self) -> None:
    self.tokens: list[Token] = []

  def tk(self) -> Token:
    """return current token in parser"""
    return self.tokens[0]

  def eat(self, tokentype: TokenType) -> Token:
    if self.tk().type == tokentype:
      return self.tokens.pop(0)
    raise Exception(__file__, f'Token {tokentype.name} not found.')

  def parse(self, code: str) -> Program:
    self.tokens = tokenize(code)

    return self.parse_program()

  def parse_program(self) -> Program:
    """
      program: scope*
    """
    program: Program = Program()

    while self.tk().type != TokenType.EOF:
      program.body.append(self.parse_scope())
    
    return program
  
  def parse_scope(self) -> Stmt:
    """
      scope: OPEN_BRACE stmt_list CLOSE_BRACE
           | stmt_list
    """
    if self.tk().type == TokenType.OPEN_BRACE:
      self.eat(TokenType.OPEN_BRACE)
      result = self.parse_stmt_list()
      self.eat(TokenType.CLOSE_BRACE)
      return result
  
    return self.parse_stmt_list()

  def parse_stmt_list(self) -> Stmt:
    """
      stmt_list: stmt
               | stmt SEMICOLON stmt_list
    """

    result = self.parse_stmt()
    if self.tk().type == TokenType.SEMICOLON:
      self.eat(TokenType.SEMICOLON)
      result = self.parse_stmt_list()

    return result

  def parse_stmt(self) -> Stmt:
    """
      stmt: scope
          | declaration_stmt
          | assignment_stmt
          | expression
    """
    if self.tk().type == TokenType.OPEN_BRACE:
      return self.parse_scope()
    elif self.tk().type == TokenType.LET:
      return self.parse_declaration_stmt()
    elif self.tk().type == TokenType.IDENTIFIER and self.tokens[1].type == TokenType.EQUALS:
      return self.parse_assignment_stmt()
    else:
      return self.parse_expression()
  
  def parse_declaration_stmt(self) -> DeclarationStmt:
    """
      declaration: LET identifier EQUALS expr
    """
    self.eat(TokenType.LET)
    left = self.parse_variable_factor()
    self.eat(TokenType.EQUALS)
    right = self.parse_expression()

    return DeclarationStmt(left, right)

  def parse_assignment_stmt(self) -> AssignmentStmt:
    """
      declaration: variable_factor EQUALS expr
    """
    left = self.parse_variable_factor()
    self.eat(TokenType.EQUALS)
    right = self.parse_expression()

    return AssignmentStmt(left, right)

  def parse_expression(self) -> Expr:
    """
      expr: binary_expr
    """
    return self.parse_binary_expr()
  
  def parse_binary_expr(self) -> Expr:
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
      operator = self.eat(TokenType.OPERATER).value
      right = self.parse_multiplicative_expr()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_multiplicative_expr(self) -> Expr:
    """
      multiplicative_expr: factor ((MUL | DIV) factor)*
    """
    left = self.parse_factor()

    while self.tk().value == '*' or self.tk().value == '/':
      operator = self.eat(TokenType.OPERATER).value
      right = self.parse_factor()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_unary_expr(self) -> Expr:
    operator = self.eat(TokenType.OPERATER).value

    if operator == '+' or operator == '-':
      result = self.parse_factor()

      if issubclass(result.__class__, NumberFactor):
        if operator == '+':
          result = cast(NumberFactor, result)
          result.value = result.value
        elif operator == '-':
          result = cast(NumberFactor, result)
          result.value = -result.value
      else:
        raise Exception(__file__, 'Not number factor.', result.__class__)
    else:
      raise Exception(__file__, 'Unknow unary expr.')

    return result
  
  def parse_factor(self) -> Expr:
    """
      factor: (PLUS | MINUS) factor
            | number_factor
            | variable_factor
            | OPEN_PAREN expr CLOSE_PAREN
    """
    if self.tk().type == TokenType.OPERATER \
      and (self.tk().value == '+' or self.tk().value == '-'):
      return self.parse_unary_expr()
    elif self.tk().type == TokenType.NUMBER:
      return self.parse_number_factor()
    elif self.tk().type == TokenType.IDENTIFIER:
      return self.parse_variable_factor()
    elif self.tk().type == TokenType.OPEN_PAREN:
      self.eat(TokenType.OPEN_PAREN)
      value = self.parse_expression()
      self.eat(TokenType.CLOSE_PAREN)
      return value
    else:
      return NullFactor()
    
  def parse_number_factor(self) -> NumberFactor:
    """
      number_factor: NUMBER
    """
    return NumberFactor(int(self.eat(TokenType.NUMBER).value))

  def parse_variable_factor(self) -> VariableFactor:
    """
      variable_factor: IDENTIFIER
    """
    return VariableFactor(self.eat(TokenType.IDENTIFIER).value)
