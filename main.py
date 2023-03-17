import frontend
import backend


def repl():
  print('JRF - v0.1.0')

  while True:  
    code = input('~ > ')
    if code == 'exit':
      return
    
    parser = frontend.Parser()
    interpreter = backend.Interpreter()
    
    program = parser.parse(code)
    result = interpreter.interpret(program)

    print(result)

if __name__ == '__main__':
  repl()