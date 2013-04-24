import csv, re
from dateutil import rrule
from datetime import date, timedelta
from random import choice, sample, randrange, normalvariate, random
from collections import namedtuple

SALES_STDDEV = 4000

MIN_CALORIES = 150
MAX_CALORIES = 1500

PRICE_STDDEV = 150  # $1.50
MIN_PRICE = 200     # $2
MAX_PRICE = 1000    # $10

NUM_TOTAL_COMBOS = 6

START_DATE = date(2008, 1, 1)
END_DATE = date(2012, 1, 1)

chars = re.compile(r'[^\w\s\-.]')

foods = [chars.sub('', l.strip()) for l in open('foods.txt')]
adjectives = [chars.sub('', l.strip()) for l in open('adjectives.txt')]
ideologies = [chars.sub('', l.strip()) for l in open('ideologies.txt')]

countries = [
  'Australia',
  'New Zealand',
  'Singapore'
]

suppliers = [
  'Greenham Suppliers Incorporated',
  'Tyndall Wholefoods and Logistics Pty Ltd'
]

ftypes = [
  'Dine-in',
  'Drive-through',
  'Both'
]

idesigns = [
  'Avant-garde',
  'Upside-down',
  'No roof',
]

speriods = [
  'Breakfast',
  'Lunch',
  'Dinner'
]

def random_store_name():
  return ('The %s %s Store' % (choice(adjectives), choice(ideologies)) ).title()
  
def random_combo_name():
  return ('%s %s Combo' % (choice(adjectives), choice(foods)) ).title()
  
Combo = namedtuple('Combo', ['name', 'calories', 'supplier', 'meanprice'])
PricedCombo = namedtuple('PricedCombo', ['combo', 'price'])
Store = namedtuple('Store', ['name', 'country', 'design', 'type'])

# Returns number of sales a store has for a given speriod of promotion period
def store_sales_magic(store, period):
  avgsales = { # Average sales by store facilities
    'Dine-in': 50000,
    'Drive-through': 70000,
    'Both': 100000,
  }
  
  design = { # Design factor influencing sales on restaurants offering dine-in
    'Avant-garde': 1.2, # People love art
    'Upside-down': 1.0, # People have no opinion on being upside-down
    'No roof': 0.7, # People hate getting wet
  }
  
  country = { # Countries influencing
    'Australia': 1.0,
    'New Zealand': 1.2,
    'Singapore': 0.9,  
  }
  
  csales = avgsales[store.type] * country[store.country]
  
  if store.type == 'Drive-through': # Drive-through isn't affected by store design
    return normalvariate(csales, SALES_STDDEV)
  else:
    return normalvariate(csales * design[store.design], SALES_STDDEV)

# Recieves data like: [PricedCombo, PricedCombo]
# Returns tuple indicating the ratio of sales of combo 1 to combo 2
def customer_decision_magic(c):
  c0ratio = 1.0 # Calorie ratio
  p0ratio = 1.0 # Price ratio
  ratio0 = 1.0 # Overall ratio
  
  # Caloric ratio
  if c[0].combo.calories > c[1].combo.calories:
    c0ratio = c[1].combo.calories / c[0].combo.calories
    c0ratio = 1 - c0ratio
  else:
    c0ratio = c[0].combo.calories / c[1].combo.calories  
    
  # Price ratio
  if c[0].price > c[1].price:
    p0ratio = c[1].price / c[0].price
    p0ratio = 1 - p0ratio
  else:
    p0ratio = c[0].price / c[1].price
    
  # Overall ratio is halfway between price and calorie ratio
  ratio0 = (c0ratio + p0ratio) / 2
  
  # Tyndall has superior ingredients
  if c[0].combo.supplier != c[1].combo.supplier:
    if c[0].combo.supplier == 'Tyndall Wholefoods and Logistics Pty Ltd':
      ratio0 *= 1.125
    else:
      ratio0 *= 0.875
  
  return (ratio0, 1-ratio0)

# Generate stores
stores = []
for country in countries:
  for store in [random_store_name() for _ in range(3)]:
    design = choice(idesigns)
    type = choice(ftypes)
    stores.append(
      Store(
        store,    # Name
        country,  # Country
        design,   # Design
        type      # Type
       )
    )

with open('fulldata.csv', 'w', newline='') as fcsv:
  
  fw = csv.writer(fcsv)
  fw.writerow(( # Write out the identification rows
    'StoreName',
    'StoreCountry',
    'StoreDesign',
    'StoreFacilities',
    
    'SalesPeriod',
    'PromotionalPeriod',
    'SalesYear',
    
    'ComboName',
    'ComboSupplier',
    'ComboCalories',
    'ComboNumSales',
    'ComboPriceCents'
  ))
  
  globalcombos = [] # Stores the current combos that are available
  storecombos = {} # Stores which combos a given store has for a given sales period
  
  # Iterate over ever day from START_DATE to END_DATE
  for dt in rrule.rrule(rrule.MONTHLY, bymonth=(1,2,3,4,5,6), dtstart=START_DATE, until=END_DATE):
    # Regen global combo list
    globalcombos = []
    for i in range(NUM_TOTAL_COMBOS):
      combo = (
        random_combo_name(),                    # Name
        randrange(MIN_CALORIES, MAX_CALORIES),  # Calories
        suppliers[i%len(suppliers)],            # Supplier
        randrange(MIN_PRICE, MAX_PRICE),        # Mean price
      )
      
      globalcombos.append(Combo(name=combo[0], calories=combo[1], supplier=combo[2], meanprice=combo[3]))
      
    for store in stores: # For each store
      # Repick store combos
      storecombos[store.name] = {} # Create dict for store
      
      for period in speriods:
        rci = sample(range(len(globalcombos)), 2) # Pick two random unique numbers between 1-6
        
        # Turn random numbers into combos
        rc = ( globalcombos[rci[0]], globalcombos[rci[1]] )
        
        # Store combos along with a price that is normally variate from the mean price
        storecombos[store.name][period] = (
          PricedCombo(rc[0], int(normalvariate(rc[0].meanprice, PRICE_STDDEV))),
          PricedCombo(rc[1], int(normalvariate(rc[1].meanprice, PRICE_STDDEV))),
        )
  
      for period in speriods: # For each sales period
        combos = storecombos[store.name][period]
        
        # We work out how many sales a store recieves per day period per month using magic
        sales = store_sales_magic(store, period)
        
        # We work out what ratio of sales go to each combo using magic
        ratio1, ratio2 = customer_decision_magic(combos)
      
        # Write out sales of combo 1
        fw.writerow((
          store.name,
          store.country,
          store.design,
          store.type,
          
          period,
          dt.month,
          dt.year,
          
          combos[0].combo.name,
          combos[0].combo.supplier,
          combos[0].combo.calories,
          int(sales*ratio1),
          combos[0].price,
        ))
         
        # Write out sales of combo 2
        fw.writerow((
          store.name,
          store.country,
          store.design,
          store.type,
          
          period,
          dt.month,
          dt.year,
          
          combos[1].combo.name,
          combos[1].combo.supplier,
          combos[1].combo.calories,
          int(sales*ratio2),
          combos[1].price,
        ))
    
   