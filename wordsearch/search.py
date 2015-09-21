#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import time
import re

def usage():
  print("search.py [ -i | -w | -p ] filename")


def search(filename, query, option):
  if option['wordSearch']:
    flags = 0
    if (not option['caseSensitive']):
      flags = re.IGNORECASE
    pattern = re.compile(r'\b({0})\b'.format(query), flags=flags)

  with open(filename) as f:
    numFound, lineNo = 0, 0
    for line in f:
      lineNo = lineNo + 1
      found = False
      if option['wordSearch']:
        if pattern.search(line):
          found = True
      else:
        if not option['caseSensitive']:
          query, line = query.lower(), line.lower()
        if query in line:
          found = True
      if found:
        if option['print']:
          sys.stdout.write('%d ' % lineNo)
        numFound = numFound + 1
  return numFound


def main(args):
  option = {
    'caseSensitive': True,  # 대소문자 구별을 할까?
    'wordSearch': False,    # 단어 단위로 검색을 할까?
    'print': False          # 발견된 줄 번호를 출력할까?
  }

  try:
    opts, args = getopt.getopt(args, 'iwp')
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  for opt, arg in opts:
    if opt == "-i":
      option['caseSensitive'] = False
    elif opt == "-w":
      option['wordSearch'] = True
    elif opt == "-p":
      option['print'] = True

  if not args:
    usage()
    sys.exit(2)

  filename = args[0]

  # 필요하면 여기에서 Preprocessing을 할 수 있을 듯.
  
  try:
    while(True):
      query = raw_input('Enter a query: ')
      start = time.time()
      numFound = search(filename, query, option)
      stop = time.time()
      print "\nFound %d lines, %f seconds elapsed.\n\n" % (numFound, stop - start)
  except (EOFError, KeyboardInterrupt):
      print
      sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])