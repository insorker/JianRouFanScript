from typing import cast
from .ast import AssignmentStmt, BinaryExpr, DeclarationStmt, Expr, Scope, VariableFactor, NullFactor, NumberFactor, Program, Stmt
from .lexer import Token, TokenType, tokenize


class Parser:
  def __init__(self) -> None:
    self.tokens: list[Token] = []

  def _tk(self) -> Token:
    """return current token in parser"""
    return self.tokens[0]

  def _eat(self, tokentype: TokenType) -> Token:
    if self._tk().type == tokentype:
      return self.tokens.pop(0)
    raise Exception(__file__, f'Token {tokentype.name} not found.')

  def parse(self, code: str) -> Program:
    self.tokens = tokenize(code)

    return self.parse_program()

  def parse_program(self) -> Program:
    """
      program: (scope | stmt_list)*
    """
    program: Program = Program()

    while self._tk().type != TokenType.EOF:
      if self._tk().type == TokenType.OPEN_BRACE:
        program.body.append(self.parse_scope())
      else:
        program.body += self.parse_stmt_list()
    
    return program
  
  def parse_scope(self) -> Scope:
    """
      scope: OPEN_BRACE stmt_list CLOSE_BRACE
    """
    scope = Scope()
    self._eat(TokenType.OPEN_BRACE)
    scope.body += self.parse_stmt_list()
    self._eat(TokenType.CLOSE_BRACE)
    return scope

  def parse_stmt_list(self) -> list:
    """
      stmt_list: stmt
               | stmt (SEMICOLON stmt)*
    """
    node = [ self.parse_stmt() ]

    while self._tk().type == TokenType.SEMICOLON:
      self._eat(TokenType.SEMICOLON)
      node.append(self.parse_stmt())

    return node

  def parse_stmt(self) -> Scope | Stmt:
    """
      stmt: scope
          | declaration_stmt
          | assignment_stmt
    """
    if self._tk().type == TokenType.OPEN_BRACE:
      return self.parse_scope()
    elif self._tk().type == TokenType.LET:
      return self.parse_declaration_stmt(False)
    elif self._tk().type == TokenType.CONST:
      return self.parse_declaration_stmt(True)
    else:
      return self.parse_assignment_stmt()
  
  def parse_declaration_stmt(self, const: bool) -> DeclarationStmt:
    """
      declaration: LET identifier EQUALS expr
    """
    self._eat(TokenType.LET)
    left = self.parse_variable_factor()
    self._eat(TokenType.EQUALS)
    right = self.parse_expr()

    return DeclarationStmt(left, right, const)

  def parse_assignment_stmt(self) -> AssignmentStmt | Expr:
    """
      assignment: expr (EQUALS expr)?
    """
    left = self.parse_expr()

    if self._tk().type == TokenType.EQUALS:
      self._eat(TokenType.EQUALS)
      right = self.parse_expr()
      return AssignmentStmt(left, right)
    else:
      return left

  def parse_expr(self) -> Expr:
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

    while self._tk().value == '+' or self._tk().value == '-':
      operator = self._eat(TokenType.OPERATER).value
      right = self.parse_multiplicative_expr()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_multiplicative_expr(self) -> Expr:
    """
      multiplicative_expr: factor ((MUL | DIV) factor)*
    """
    left = self.parse_factor()

    while self._tk().value == '*' or self._tk().value == '/':
      operator = self._eat(TokenType.OPERATER).value
      right = self.parse_factor()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_unary_expr(self) -> Expr:
    operator = self._eat(TokenType.OPERATER).value

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
    if self._tk().type == TokenType.OPERATER \
      and (self._tk().value == '+' or self._tk().value == '-'):
      return self.parse_unary_expr()
    elif self._tk().type == TokenType.NUMBER:
      return self.parse_number_factor()
    elif self._tk().type == TokenType.IDENTIFIER:
      return self.parse_variable_factor()
    elif self._tk().type == TokenType.OPEN_PAREN:
      self._eat(TokenType.OPEN_PAREN)
      value = self.parse_expr()
      self._eat(TokenType.CLOSE_PAREN)
      return value
    else:
      return NullFactor()
    
  def parse_number_factor(self) -> NumberFactor:
    """
      number_factor: NUMBER
    """
    return NumberFactor(int(self._eat(TokenType.NUMBER).value))

  def parse_variable_factor(self) -> VariableFactor:
    """
      variable_factor: IDENTIFIER
    """
    return VariableFactor(self._eat(TokenType.IDENTIFIER).value)
