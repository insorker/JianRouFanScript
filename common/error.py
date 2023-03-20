from enum import Enum

class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND     = 'Identifier not found'
    DUPLICATE_ID     = 'Duplicate id found'


class Error(Exception):
  def __init__(self, message=None):
    super().__init__(f'{self.__class__.__name__}: {message}')


class LexerError(Error):
  pass


class ParserError(Error):
  pass


class SemanticError(Error):
  pass