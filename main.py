import frontend
# import backend


def repl():
  print('JRF - v0.2.0')
  lexer = frontend.Lexer()
  parser = frontend.Parser()
  semantic_analyzer = frontend.SemanticAnalyzer()
  # interpreter = backend.Interpreter()

  while True:  
    code = input('~ > ')
    if code == 'exit':
      return

    tokens = lexer.tokenize(code)
    program = parser.parse(tokens)
    program = semantic_analyzer.visit(program)
    # result = interpreter.interpret(program)

    print(program)
    print(program.symtab)
    # print(program)
    # print(result)

def run():
  with open('main.jrf', 'r') as f:
    parser = frontend.Parser()
    interpreter = backend.Interpreter()

    program = parser.parse(f.read())
    result = interpreter.interpret(program)

    print(program)
    print(result)

if __name__ == '__main__':
  # run()
  repl()