from enum import Enum, auto
import re

class TokenType(Enum):
  NUMBER = auto()
  STRING = auto()
  IDENTIFIER = auto()
  
  LET = auto()

  BINARY_OPERATOR = auto()
  EQUALS = auto()
  OPEN_PAREN = auto()
  CLOSE_PAREN = auto()

  SPACE = auto()
  EOF = auto()

TOKEN_REGEX = {
  TokenType.NUMBER:           r'[1-9][0-9]*',
  TokenType.IDENTIFIER:       r'[a-zA-Z_]+[a-zA-Z_0-9]*',
  TokenType.STRING:           r'["].*?["]',
  TokenType.LET:              r'let',
  TokenType.BINARY_OPERATOR:  r'[+\-*/%]',
  TokenType.EQUALS:           r'=',
  TokenType.OPEN_PAREN:       r'\(',
  TokenType.CLOSE_PAREN:      r'\)',
  TokenType.SPACE:            r'[ \t\r]+',
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
        if tokentype != TokenType.SPACE:
          tokens.append(Token(tokentype, value))
        break
        
    if not match:
      raise Exception(__file__, 'No valid match: ', code)

  tokens.append(Token(TokenType.EOF, 'EOF'))

  return tokens

while True:
  src = input('>>>')
  tokens = tokenize(src)
  for token in tokens:
    print(token)