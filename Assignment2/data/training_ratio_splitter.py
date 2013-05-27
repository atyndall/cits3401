# Simple Python 2.7 script to split data into N sets of equal ratios, where Royal Flush is the split point
from collections import defaultdict
import os

IN_FILE = 'poker-hand-training.arff'
OUT_DIR = 'poker-hand-training-split'

cdict = defaultdict(list) # Contains all pairs, indexed by class

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
    sline = line.strip()
    pclass = sline[sline.rindex(',')+1:] # Class is the last attribute after last comma
    cdict[pclass].append(sline)
    line = f.readline()
    
  # All lines are now read into memory
  # Calculate ratios
  
  num_rf = len(cdict['RF'])
  
  ratios = {'RF': 1}
  
  for type, values in cdict.iteritems():
    lv = len(values)
    if type != 'RF':
      ratios[type] = lv/num_rf
      
  for i in range(num_rf):
    path = os.path.join(OUT_DIR, "%d-%s" % (i, IN_FILE))
    with open(path, 'w') as outf:
      outf.write("\n".join(header) + "\n")
      for type, number in ratios.iteritems():
        sublist = cdict[type][(i*number):((i*number)+number)]
        outf.write("\n".join(sublist) + "\n")