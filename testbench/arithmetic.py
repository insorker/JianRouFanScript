import random

def gen_int(n) -> int:
  return random.randint(0, n)

def gen_float(n) -> float:
  return n * random.random()

def gen_op(le=0, ri=4):
  op = '+-*/%'
  idx = random.randint(le, ri)
  return op[idx]

def gen_int_add(n):
  result = ''
  op = random.randint(0, n)

  while op != 0:
    op = random.randint(0, 1)
    result += str(gen_int(1000)) + gen_op(0, 1) + gen_int_add(n)
  
  return result

def gen_int_mul(n):
  result = ''
  op = random.randint(0, n)

  while op != 0:
    op = random.randint(0, 1)
    result += str(gen_int(1000)) + gen_op(2, 4) + gen_int_add(n)
  
  return result

def gen_int_expr(n):
  op = random.randint(0, n)