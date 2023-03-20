import frontend
from symtab.symboltablebuilder import SymbolTableBuilder
# import backend


def repl():
  print('JRF - v0.2.0')
  parser = frontend.Parser()
  symtab_builder = SymbolTableBuilder()
  # interpreter = backend.Interpreter()

  while True:  
    code = input('~ > ')
    if code == 'exit':
      return

    program = parser.parse(code)
    program = symtab_builder.visit_Program(program)
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