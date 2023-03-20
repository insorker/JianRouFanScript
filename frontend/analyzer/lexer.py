from enum import Enum, auto
import re


class TokenType(Enum):
  LET = auto()
  CONST = auto()
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
  TokenType.COMMENT: r'//[^\n]*',
  TokenType.INTEGER: r'[1-9]+[0-9]*|0',
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
  def __init__(self, type: TokenType, value: str) -> None:
    self.type: TokenType = type
    self.value: str = value
  
  def __repr__(self):
    return f'{{ {self.type}, {self.value} }}'


class Lexer:
  def tokenize(self, code: str) -> list[Token]:
    tokens: list[Token] = []
    match = None

    while code:
      for tokentype, pattern in TOKEN_REGEX.items():
        match = re.match(pattern, code)

        if match:
          value = match.group()
          code = code[len(value):]

          if tokentype == TokenType.SPACE:
            pass
          elif tokentype == TokenType.COMMENT:
            pass
          elif tokentype == TokenType.STRING:
            tokens.append(Token(tokentype, value[1:-1]))
          else:
            tokens.append(Token(tokentype, value))
          
          break

      if match == None:
        raise Exception(__file__, 'Not valid charater: ' + code[0])

    tokens.append(Token(TokenType.EOF, 'EOF'))
    return tokens