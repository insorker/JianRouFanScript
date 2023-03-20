from typing import cast
from frontend.ast import *
from frontend.lexer import Token, TokenType


class Parser:
  def __init__(self) -> None:
    self.tokens: list[Token] = []

  def _tk(self) -> Token:
    """return current token"""
    return self.tokens[0]

  def _eat(self, tokentype: TokenType | None) -> Token:
    """eat and return current token if type matches"""
    if tokentype == None:
      return self.tokens.pop(0)
    if self._tk().type == tokentype:
      return self.tokens.pop(0)
    
    raise Exception(__file__, f'Token {tokentype.name} not found.')

  def parse(self, tokens: list[Token]) -> Program:
    """return the ast of code"""
    self.tokens = tokens

    return self.parse_program()

  def parse_program(self) -> Program:
    """
      program: (block | stmt_list)*
    """
    program: Program = Program()

    while self._tk().type != TokenType.EOF:
      if self._tk().type == TokenType.OPEN_BRACE:
        program.body.append(self.parse_block())
      else:
        program.body += self.parse_stmt_list()
    
    return program
  
  def parse_block(self) -> Block:
    """
      block: OPEN_BRACE stmt_list CLOSE_BRACE
    """
    block = Block()
    self._eat(TokenType.OPEN_BRACE)
    block.body += self.parse_stmt_list()
    self._eat(TokenType.CLOSE_BRACE)
    return block

  def parse_stmt_list(self) -> list:
    """
      stmt_list: stmt (SEMICOLON stmt)*
    """
    node = self.parse_stmt()

    while self._tk().type == TokenType.SEMICOLON:
      self._eat(TokenType.SEMICOLON)
      node += self.parse_stmt()

    return node

  def parse_stmt(self) -> list[Block] | list[Stmt] | list[Expr]:
    """
      stmt: blcok
          | variable_declaration_stmt
          | assignment_expr
    """
    if self._tk().type == TokenType.OPEN_BRACE:
      return [self.parse_block()]
    elif self._tk().type == TokenType.LET:
      return self.parse_variable_declaration_stmt(False)
    elif self._tk().type == TokenType.CONST:
      return self.parse_variable_declaration_stmt(True)
    else:
      return self.parse_assignment_expr()
  
  def parse_variable_declaration_stmt(self, const: bool) -> list[Stmt]:
    """
      variable_declaration_stmt: (LET | CONST) assignment_stmt
    """
    self._eat(self._tk().type)
    
    result = []
    expr_list = self.parse_assignment_expr()

    for expr in expr_list:
      if type(expr) == AssignmentExpr:
        expr = cast(AssignmentExpr, expr)
        result.append(VarDeclarationStmt(expr.left, expr.right, const))
      else:
        result.append(VarDeclarationStmt(expr, NullFactor(), const))
    
    return result # list[VariableDeclarationStmt]

  def parse_single_assignment_expr(self) -> Expr:
    """
      single_assignment_expr: expr | expr EQUALS single_assignment_expr
    """
    left = self.parse_expr()

    while self._tk().type == TokenType.EQUALS:
      self._eat(TokenType.EQUALS)
      left = AssignmentExpr(left, self.parse_single_assignment_expr())
    
    return left

  def parse_assignment_expr(self) -> list[Expr]:
    """
      assignment_stmt: single_assignment_expr (COMMA single_assignment_expr)*
    """
    result = [ self.parse_single_assignment_expr() ]

    while self._tk().type == TokenType.COMMA:
      self._eat(TokenType.COMMA)
      result.append(self.parse_single_assignment_expr())
    
    return result

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
  
  def parse_factor(self) -> Expr:
    """
      factor: INTEGER
            | FLOAT
            | IDENTIFIER
            | OPEN_PAREN expr CLOSE_PAREN
    """
    if self._tk().type == TokenType.INTEGER:
      return IntegerFactor(Integer(int(self._eat(None).value)))
    
    elif self._tk().type == TokenType.FLOAT:
      return FloatFactor(Float(int(self._eat(None).value)))
    
    elif self._tk().type == TokenType.IDENTIFIER:
      return VarFactor(Any.__name__, self._eat(None).value)
    
    elif self._tk().type == TokenType.OPEN_PAREN:
      self._eat(TokenType.OPEN_PAREN)
      value = self.parse_expr()
      self._eat(TokenType.CLOSE_PAREN)
      return value
    
    else:
      return NullFactor()
