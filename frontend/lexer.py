from enum import Enum, auto
import re


class TokenType(Enum):
  NUMBER = auto()
  IDENTIFIER = auto()
  STRING = auto()
  BINARY_OPERATER = auto()
  EQUALS = auto()
  OPEN_PAREN = auto()
  CLOSE_PAREN = auto()
  SPACE = auto()
  EOF = auto()

TOKEN_REGEX = {
  TokenType.NUMBER: r'[1-9]+[0-9]*|0',
  TokenType.IDENTIFIER: r'[a-zA-Z_]+[a-zA-Z_0-9]*',
  TokenType.STRING: r'".*?"',
  TokenType.BINARY_OPERATER: r'[+\-*/%]',
  TokenType.EQUALS: r'=',
  TokenType.OPEN_PAREN: r'\(',
  TokenType.CLOSE_PAREN: r'\)',
  TokenType.SPACE: r'[ \t\r]',
}

class Token:
  def __init__(self, type: TokenType, value: str) -> None:
    self.type: TokenType = type
    self.value: str = value
  
  def __repr__(self):
    return f'{{ {self.type}, {self.value} }}'

def tokenize(code: str) -> list[Token]:
  tokens: list[Token] = []
  match = None

  while code:
    for tokentype, pattern in TOKEN_REGEX.items():
      match = re.match(pattern, code)

      if match:
        value = match.group()
        code = code[len(value):]

        if tokentype == TokenType.SPACE:
          continue
        elif tokentype == TokenType.STRING:
          tokens.append(Token(tokentype, value[1:-1]))
        else:
          tokens.append(Token(tokentype, value))
        break

    if match == None:
      raise Exception(__file__, 'Not valid charater: ', code[0])

  tokens.append(Token(TokenType.EOF, 'EOF'))
  return tokens