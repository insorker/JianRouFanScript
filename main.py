import frontend
import backend


lexer = frontend.Lexer()
parser = frontend.Parser()
semantic_analyzer = frontend.SemanticAnalyzer()
interpreter = backend.Interpreter()


def repl():
  print('JRF - v0.2.0')
  
  while True:  
    code = input('~ > ')
    if code == 'exit':
      return

    tokens = lexer.tokenize(code)
    program = parser.parse(tokens)
    semantic_analyzer.visit(program)
    result = interpreter.interpret(program)

    
    print(program)
    print(result)


def run():
  with open('main.jrf', 'r') as f:
    tokens = lexer.tokenize(f.read())
    program = parser.parse(tokens)
    semantic_analyzer.visit(program)
    interpreter.interpret(program)

if __name__ == '__main__':
  run()
  # repl()