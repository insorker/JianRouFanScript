import frontend


def repl():
  print('Repl v2.0:')

  while True:
    code = input('>>> ')
    if code == 'exit':
      break

    parser = frontend.Parser()
    program = parser.parse(code)

    print(program)


if __name__ == '__main__':
  repl()