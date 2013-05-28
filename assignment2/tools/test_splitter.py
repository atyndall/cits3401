# Simple Python 2.7 script to split data into N sets of N elements
import os
import random

IN_FILE = 'poker-hand-testing-allnominal-scsort.arff'
OUT_DIR = ('poker-hand-testing-split','allnominal','scsort','%d-%s')

SETS = 10
VALUES_PER_SET = 5000

list = [] # Contains all pairs

with open(IN_FILE, 'r') as f:
  
  header = []
  
  line = f.readline()
  while line.strip() != "@data":
    if line == "":
      exit("Couldn't locate the start of data")
      
    header.append(line.strip())
    line = f.readline()
    
  header.append(line.strip())
  # We've now walked the text file to the start of the data
  
  line = f.readline()
  while line != "":
    list.append(line.strip())
    line = f.readline()
    
  # All lines are now read into memory
  random.shuffle(list)
  
  for i in range(SETS):
    path = os.path.join(*OUT_DIR) % (i, IN_FILE)
    with open(path, 'w') as outf:
      outf.write("\n".join(header) + "\n")
      sublist = list[(i*VALUES_PER_SET):((i*VALUES_PER_SET)+VALUES_PER_SET)]
      outf.write("\n".join(sublist) + "\n")