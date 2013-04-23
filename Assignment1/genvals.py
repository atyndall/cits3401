import csv, re
from dateutil import rrule
from datetime import date, timedelta
from random import choice, sample, randrange, normalvariate, random
from collections import namedtuple

PRICE_STDDEV = 100
SALES_STDDEV = 25

MIN_CALORIES = 500
MAX_CALORIES = 10000

MIN_PRICE = 500
MAX_PRICE = 10000

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
  return randrange(5000, 10000)

# Recieves data like: [PricedCombo, PricedCombo]
# Returns tuple indicating the ratio of sales of combo 1 to combo 2
def customer_decision_magic(combos):
  a = random()
  b = 1 - a
  return (a, b)

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
    
   