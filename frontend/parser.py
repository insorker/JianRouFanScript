from typing import cast
from frontend.ast import *
from frontend.lexer import Token, TokenType
from common.error import ParserError


class Parser:
  def __init__(self) -> None:
    self._tokens: list[Token] = []

  def _tk(self, bias=0) -> Token:
    """return current token"""
    return self._tokens[bias]

  def _eat(self, token_type: TokenType | None) -> Token:
    """eat and return eaten token if type matches"""
    if token_type == None:
      return self._tokens.pop(0)
    if self._tk().type == token_type:
      return self._tokens.pop(0)
    
    raise ParserError(f'Token with {token_type} not found, find {self._tk()} instead, line {self._tk().lineno}')

  def parse(self, tokens: list[Token]) -> Program:
    """return ast of code"""
    self._tokens = tokens[::]
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
      stmt: block
          | fn_dclaration_stmt
          | var_declaration_stmt
          | fn_return_stmt
          | assignment_expr
    """
    if self._tk().type == TokenType.OPEN_BRACE:
      return [self.parse_block()]
    elif self._tk().type == TokenType.FUNCTION:
      return [self.parse_fn_dclaration_stmt()]
    elif self._tk().type == TokenType.LET:
      return self.parse_var_declaration_stmt(False)
    elif self._tk().type == TokenType.CONST:
      return self.parse_var_declaration_stmt(True)
    elif self._tk().type == TokenType.RETURN:
      return [self.parse_fn_return_stmt()]
    else:
      return self.parse_assignment_expr()
  
  def parse_var_declaration_stmt(self, const: bool) -> list[Stmt]:
    """
      var_declaration_stmt: (LET | CONST) assignment_stmt
    """
    self._eat(None)
    result = []

    for expr in self.parse_assignment_expr():
      if type(expr) == AssignmentExpr:
        expr = cast(AssignmentExpr, expr)
        result.append(VarDeclarationStmt(expr.left, expr.right, const))
      else:
        result.append(VarDeclarationStmt(expr, UndefinedFactor(), const))
    
    return result # list[VariableDeclarationStmt]

  def parse_fn_dclaration_stmt(self) -> FnDeclarationStmt:
    """
      fn_declaration_stmt: FUNCTION IDENTIFIER fn_params block
    """
    self._eat(TokenType.FUNCTION)
    name = self._eat(TokenType.IDENTIFIER).value
    params = self.parse_fn_params()
    block = self.parse_fn_block()

    return FnDeclarationStmt(name, '', params, block)

  def parse_fn_params(self) -> list[VarFactor]:
    """
      fn_params: OPEN_PAREN (var_factor (COMMA var_factor)*)? CLOSE_PAREN
    """
    self._eat(TokenType.OPEN_PAREN)
    result = []

    if self._tk().type != TokenType.CLOSE_PAREN:
      result.append(self.parse_var_factor())

      while self._tk().type == TokenType.COMMA:
        self._eat(TokenType.COMMA)
        result.append(self.parse_var_factor())
    
    self._eat(TokenType.CLOSE_PAREN)
    return result
  
  def parse_fn_block(self) -> FnBlock:
    """
      fn_block: OPEN_BRACE stmt_list CLOSE_BRACE
    """
    self._eat(TokenType.OPEN_BRACE)
    block = FnBlock()
    block.body = self.parse_stmt_list()
    self._eat(TokenType.CLOSE_BRACE)
    return block

  def parse_fn_return_stmt(self) -> FnReturnStmt:
    """
      fn_return_stmt: RETURN expr
    """
    self._eat(TokenType.RETURN)
    return FnReturnStmt(self.parse_expr())

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
      expr: additive_expr
    """
    return self.parse_additive_expr()

  def parse_additive_expr(self) -> Expr:
    """
      additive_expr: multiplicative_expr ((PLUS | MINUS) multiplicative_expr)*
    """
    left = self.parse_multiplicative_expr()

    while self._tk().value == '+' or self._tk().value == '-':
      operator = self._eat(None).value
      right = self.parse_multiplicative_expr()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_multiplicative_expr(self) -> Expr:
    """
      multiplicative_expr: factor ((MUL | DIV) factor)*
    """
    left = self.parse_factor()

    while self._tk().value == '*' or self._tk().value == '/' or self._tk().value == '%':
      operator = self._eat(None).value
      right = self.parse_factor()
      left = BinaryExpr(left, right, operator)
    
    return left
  
  def parse_factor(self) -> Expr:
    """
      factor: INTEGER
            | FLOAT
            | fn_call_factor
            | var_factor
            | OPEN_PAREN expr CLOSE_PAREN
            | nop_factor
    """
    if self._tk().type == TokenType.INTEGER:
      return IntegerFactor(Integer(int(self._eat(None).value)))
    
    elif self._tk().type == TokenType.FLOAT:
      return FloatFactor(Float(float(self._eat(None).value)))
    
    elif self._tk().type == TokenType.IDENTIFIER and self._tk(1).type == TokenType.OPEN_PAREN:
      return self.parse_fn_call_factor()

    elif self._tk().type == TokenType.IDENTIFIER:
      return self.parse_var_factor()
    
    elif self._tk().type == TokenType.OPEN_PAREN:
      self._eat(TokenType.OPEN_PAREN)
      value = self.parse_expr()
      self._eat(TokenType.CLOSE_PAREN)
      return value
    
    else:
      return self.parse_nop_factor()
      
  def parse_fn_call_factor(self) -> Factor:
    """
      fn_call_factor: IDENTIFIER OPEN_PAREN (expr (COMMA expr)*)? CLOSE_PAREN
    """
    name = self._eat(TokenType.IDENTIFIER).value
    params = []
    self._eat(TokenType.OPEN_PAREN)
    
    if self._tk().type != TokenType.CLOSE_PAREN:
      params.append(self.parse_expr())

      while self._tk().type == TokenType.COMMA:
        self._eat(TokenType.COMMA)
        params.append(self.parse_expr())
    
    self._eat(TokenType.CLOSE_PAREN)
    return FnCallFactor(name, params)

  def parse_var_factor(self) -> VarFactor:
    """var_factor: IDENTIFIER"""
    return VarFactor(Any.__name__, self._eat(TokenType.IDENTIFIER).value)
  
  def parse_nop_factor(self) -> NopFactor:
    return NopFactor()