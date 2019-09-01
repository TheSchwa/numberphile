#!/usr/bin/env python3
#
# https://www.youtube.com/watch?v=Wim9WJeDTHQ
# https://en.wikipedia.org/wiki/Persistence_of_a_number
# https://oeis.org/A003001
#
# 0, 10, 25, 39, 77, 679, 6788, 68889, 2677889, 26888999, 3778888999, 277777788888899
#
# Example run on AMD Ryzen 7 2700X Eight-Core Processor (8C, 16T, 3.7GHz):
#
#   [laptopdude@shinkiro:~/.../numberphile] ./persistent.py 8
#   ('0.00', 0, 0)
#   ('0.00', 1, 10)
#   ('0.00', 2, 25)
#   ('0.00', 3, 39)
#   ('0.00', 4, 77)
#   ('0.00', 5, 679)
#   ('0.01', 6, 6788)
#   ('0.03', 7, 68889)
#   ('0.89', 8, 2677889)
#   ('9.56', 9, 26888999)
#   ('1427.94', 10, 3778888999)

import sys, time
from functools import reduce
from multiprocessing import Process, Queue

def main(processes=1):

  processes = int(processes)

  best = Best()
  start = 0
  for i in range(processes):
    p = Process(target=run, args=(start, processes, best.queue))
    p.start()
    start += 1
  
  try:
    while True:
      time.sleep(1)
      best.process()
  except BaseException:
    pass

class Best:

  def __init__(self):

    self.log = []
    self.printed = []
    self.queue = Queue()

  def process(self):

    had = len(self.log)

    while True:
      try:
        x = self.queue.get(False)
      except:
        break
      self.check(*x)

    have = len(self.log)

    for i in range(had, have):
      x = self.log[i]
      self.printed.append(x)
      print(x)

    for (a,b) in zip(self.printed, self.log):
      if a != b:
        print('CHANGE: %s' % (b,))
    self.printed = self.log[:]

  def check(self, t, num, steps):

    if steps == len(self.log):
      self.log.append(('%.2f' % t, steps, num))
    elif num < self.log[steps][2]:
      self.log[steps] = ('%.2f' % t, steps, num)

def run(start, increment, queue):

  i = start
  best = -1
  born = time.time()
  try:
    while True:
      steps = per(str(i))
      if steps > best:
        queue.put((time.time()-born, i, steps))
        best = steps
      i += increment
  except KeyboardInterrupt:
    pass

def per(x):

  if len(x) == 1:
    return 0

  result = reduce(lambda a,b: a*int(b), x, 1)
  return 1 + per(str(result))

if __name__ == '__main__':
  main(*sys.argv[1:])
