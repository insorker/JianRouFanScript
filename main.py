import frontend
import backend


def repl():
  print('JRF - v0.2.0')
  parser = frontend.Parser()
  interpreter = backend.Interpreter()

  while True:  
    code = input('~ > ')
    if code == 'exit':
      return

    program = parser.parse(code)
    result = interpreter.interpret(program)

    print(result)

def run():
  with open('main.jrf', 'r') as f:
    parser = frontend.Parser()
    interpreter = backend.Interpreter()

    program = parser.parse(f.read())
    # result = interpreter.interpret(program)

    print(program)
    # print(result)

if __name__ == '__main__':
  run()
  # repl()