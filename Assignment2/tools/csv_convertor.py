# Simple Python 2.7 script to covert the poker data sets to something more useful
import csv

IN_FILE = 'poker-hand-training.txt'
OUT_FILE = 'poker-hand-training.arff'

append = '''@relation poker_hand

@attribute S1 {H, S, D, C}
@attribute C1 numeric
@attribute S2 {H, S, D, C}
@attribute C2 numeric
@attribute S3 {H, S, D, C}
@attribute C3 numeric
@attribute S4 {H, S, D, C}
@attribute C4 numeric
@attribute S5 {H, S, D, C}
@attribute C5 numeric
@attribute CLASS {0, 1, 2, 3, S, F, FH, 4, SF, RF}


@data
'''

suite_map = { # Initial value : New value
  1: 'H',
  2: 'S',
  3: 'D',
  4: 'C',
}

class_map = { # Initial value : New value
  0: 0,
  1: 1,
  2: 2,
  3: 3,
  4: 'S',
  5: 'F',
  6: 'FH',
  7: 4,
  8: 'SF',
  9: 'RF',
}

map = { # Column number : Mapping algorithm (None == no mapping)
  0: suite_map,
  1: None,
  2: suite_map,
  3: None,
  4: suite_map,
  5: None,
  6: suite_map,
  7: None,
  8: suite_map,
  9: None,
  10: class_map,
}

with open(IN_FILE, 'rb') as fin:
  cin = csv.reader(fin)
  with open(OUT_FILE, 'wb') as fout:
    fout.write(append)
    cout = csv.writer(fout, delimiter=',')
    
    print "Now running... this could take a while"
    
    for rin in cin:
      rout = []
      for i, e in enumerate(rin):
        e = e.strip()
        if e.isdigit():
          e = int(e)
        if map[i]:
          rout.append(str(map[i][e]))
        else:
          rout.append(str(e))
      cout.writerow(rout)