import frontend
import backend


def repl():
  print('JRF - v0.1.0')
  parser = frontend.Parser()
  interpreter = backend.Interpreter()

  while True:  
    code = input('~ > ')
    if code == 'exit':
      return

    program = parser.parse(code)
    result = interpreter.interpret(program)

    print(result)

if __name__ == '__main__':
  repl()