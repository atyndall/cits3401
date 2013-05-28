# Simple Python 2.7 script to reorder data
from collections import defaultdict
from contextlib import nested
from operator import itemgetter
from itertools import chain
import os
import csv

# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python#answer-312464
def chunks(l, n):
  """ Yield successive n-sized chunks from l.
  """
  for i in xrange(0, len(l), n):
    yield l[i:i+n]

IN_FILE = 'poker-hand-testing-allnominal.arff'
OUT_FILE = 'poker-hand-testing-allnominal-%ssort.arff'

cdict = defaultdict(list) # Contains all pairs, indexed by class

sconv = {
  'H': 1,
  'S': 2,
  'D': 3,
  'C': 4,
}

with open(IN_FILE, 'rb') as f:
  header = []
  
  line = f.readline()
  while line.strip() != "@data":
    if line == "":
      exit("Couldn't locate the start of data")
      
    header.append(line.strip())
    line = f.readline()
    
  header.append(line.strip())
  
  # We've now walked the text file to the start of the data
  
  cr = csv.reader(f)
  with nested( open(OUT_FILE % 'sc', 'wb'), open(OUT_FILE % 'cs', 'wb') ) as (scoutf, csoutf):

    scw = csv.writer(scoutf)
    csw = csv.writer(csoutf)
    
    headtxt = "\n".join(header) + "\n"
    
    scoutf.write(headtxt)
    csoutf.write(headtxt)

    for line in cr:
      cards = [(s, c) for s, c in chunks(line[:-1], 2)]
      
      scsort = sorted(cards, key=lambda x: (sconv[x[0]], int(x[1])))
      cssort = sorted(cards, key=lambda x: (int(x[1]), sconv[x[0]]))
   
      scw.writerow(list(chain.from_iterable(scsort)) + [line[-1]])
      csw.writerow(list(chain.from_iterable(cssort)) + [line[-1]])