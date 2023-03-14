import frontend


def repl():
  while True:
    print('JRF - v0.1.0')
    code = input('~ > ')
    if code == 'exit':
      return
    
    parser = frontend.Parser()
    program = parser.parse(code)

    print(program)

if __name__ == '__main__':
  repl()