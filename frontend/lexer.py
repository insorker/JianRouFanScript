from enum import Enum, auto
import re
from common.error import LexerError


class TokenType(Enum):
  LET = auto()
  CONST = auto()
  FUNCTION = auto()
  COMMENT = auto()

  INTEGER = auto()
  FLOAT = auto()
  IDENTIFIER = auto()
  STRING = auto()
  
  OPERATER = auto()
  EQUALS = auto()

  OPEN_PAREN = auto()
  CLOSE_PAREN = auto()
  OPEN_BRACE = auto()
  CLOSE_BRACE = auto()
  SEMICOLON = auto()
  COMMA = auto()

  SPACE = auto()
  EOF = auto()


TOKEN_REGEX = {
  TokenType.LET: r'let',
  TokenType.CONST: r'const',
  TokenType.FUNCTION: r'def',
  TokenType.COMMENT: r'//[^\n]*',
  TokenType.INTEGER: r'[1-9]+[0-9]*|0',
  TokenType.FLOAT: r'([0-9]*[.])?[0-9]+',
  TokenType.IDENTIFIER: r'[a-zA-Z_]+[a-zA-Z_0-9]*',
  TokenType.STRING: r'".*?"',
  TokenType.OPERATER: r'[+\-*/%]',
  TokenType.EQUALS: r'=',
  TokenType.OPEN_PAREN: r'\(',
  TokenType.CLOSE_PAREN: r'\)',
  TokenType.OPEN_BRACE: r'{',
  TokenType.CLOSE_BRACE: r'}',
  TokenType.COMMA: r',',
  TokenType.SEMICOLON: r'[;\n]',
  TokenType.SPACE: r'[ \t\r]',
}


class Token:
  def __init__(self, type: TokenType, value: str, lineno: int) -> None:
    self.type: TokenType = type
    self.value: str = value
    self.lineno: int = lineno
  
  def __repr__(self):
    return f'{{ {self.type}, {self.value} }}'


class Lexer:
  def __init__(self) -> None:
    self.current_char = ''
    self.lineno = 1
  
  def _error(self):
    message = "Unknow character '{lexeme}', line {lineno}".format(
      lexeme=self.current_char, lineno=self.lineno,
    )
    raise LexerError(message)

  def tokenize(self, code: str) -> list[Token]:
    tokens: list[Token] = []
    match = None

    while code:
      self.current_char = code[0]

      for tokentype, pattern in TOKEN_REGEX.items():
        match = re.match(pattern, code)

        if match:
          value = match.group()
          code = code[len(value):]

          if tokentype == TokenType.SPACE:
            pass
          elif tokentype == TokenType.COMMENT:
            pass
          elif tokentype == TokenType.SEMICOLON and value == '\n':
            self.lineno += 1
            tokens.append(Token(tokentype, value, self.lineno))
          elif tokentype == TokenType.STRING:
            tokens.append(Token(tokentype, value[1:-1], self.lineno))
          else:
            tokens.append(Token(tokentype, value, self.lineno))
          
          break

      if match == None:
        raise LexerError(f"Unknow character '{self.current_char}', line {self.lineno}")

    tokens.append(Token(TokenType.EOF, 'EOF', self.lineno))
    return tokens