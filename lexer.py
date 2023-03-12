from enum import Enum, auto

class TokenType(Enum):
  # literal type
  NUMBER = auto()
  IDENTIFIER = auto()

  # keyword
  LET = auto()

  # binary operator
  BINARY_OPERATOR = auto()
  EQUALS = auto()

  # parenthesis
  OPEN_PAREN = auto()
  CLOSE_PAREN = auto()

  # end of file
  EOF = auto()

class Token:
  def __init__(self, type: TokenType, value: str) -> None:
    self.type = type
    self.value = value
  
  def __repr__(self):
    return f'{{ {self.type}, {self.value} }}'

def tokenize(srcCode: str) -> list[Token]:
  tokens: list[Token] = []
  letters = list(srcCode)

  while (len(letters) > 0):
    if letters[0] == '(':
      tokens.append(Token(TokenType.OPEN_PAREN, letters.pop(0)))
    elif letters[0] == ')':
      tokens.append(Token(TokenType.CLOSE_PAREN, letters.pop(0)))
    elif letters[0] == '+'or letters[0] == '-' or letters[0] == '*' or letters[0] == '/':
      tokens.append(Token(TokenType.BINARY_OPERATOR, letters.pop(0)))
    elif letters[0] == '=':
      tokens.append(Token(TokenType.EQUALS, letters.pop(0)))
    else:
      # number
      if letters[0].isdigit():
        value = letters.pop(0)
        while (len(letters) > 0 and letters[0].isdigit()):
          value += letters.pop(0)
        tokens.append(Token(TokenType.NUMBER, value))
      # identifier
      elif letters[0].isalpha() or letters[0] == '_':
        value = letters.pop(0)
        while (len(letters) > 0 and (letters[0].isalpha() or letters[0].isdigit() or letters[0] == '_')):
          value += letters.pop(0)
        tokens.append(Token(TokenType.IDENTIFIER, value))
      # space
      elif letters[0].isspace():
        letters.pop(0)
      else:
        raise Exception(__file__, 'Invalid character: ', letters[0])

  tokens.append(Token(TokenType.EOF, 'EOF'))

  return tokens

while True:
  src = input('>>>')
  tokens = tokenize(src)
  for token in tokens:
    print(token)