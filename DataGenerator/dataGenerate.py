#!/usr/bin/env python3

import random, csv, json, argparse, uuid, os, gzip

from bloom_filter import BloomFilter
from decimal import Decimal
from timeit import default_timer as timer
from datetime import timedelta, datetime, date
from faker import Faker
from faker.providers import profile

Faker.seed(1234)
fake = Faker()

# fake.add_provider(person)

class CustomJsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return super(CustomJsonEncoder, self).default(obj)

def getArgs():
  parser = argparse.ArgumentParser(description='Generate test data.')
  parser.add_argument('-c', '--customers', type=int, default=1000, help='#customers')
  parser.add_argument('-b', '--banks',     type=int, default=200,  help='#banks')

  parser.add_argument('-d', '--deposits',     type=int,   default=10,    help='#bank deposits')
  parser.add_argument('-k', '--cash',         type=float, default=0.15,  help='% of deposits in cash')
  parser.add_argument('-a', '--amount',       type=int, default=4000,    help='avgamount')
  parser.add_argument('-s', '--std',          type=int, default=3000,    help='stdamount')
  

  parser.add_argument('-fc', '--fcustomer', type=str, default="customer", help='filename (no extension)')
  parser.add_argument('-fd', '--fdeposits', type=str, default="deposits", help='filename (no extension)')
  parser.add_argument('-z',  '--gzip',      type=str2bool, nargs='?',const=True, default=False,help='Activate gzip.')
  args = parser.parse_args()
  return args

def genCustomerIDs(num=10, err=0.01):
  bloom = BloomFilter(max_elements=2*num, error_rate=err)
  customerIDs = set()
  for i in range(num):
    id = uuid.uuid4()
    while str(id) in bloom:
      id = uuid.uuid4()
    bloom.add(str(id))
    customerIDs.add(str(id))
  return customerIDs

def genBankIDs(num=10, err=0.01):
  bloom = BloomFilter(max_elements=2*num, error_rate=err)
  bankIDs = set()
  for i in range(num):
    id = uuid.uuid4()
    while "BANK-" + str(id) in bloom:
      id = uuid.uuid4()
    bloom.add("BANK-" + str(id))
    bankIDs.add("BANK-" + str(id))
  return bankIDs

def writeCustomers(customerIDs, fname="customer", zip=False):
  if zip:
    myOpen = gzip.open
    myMode = "wt"
    mySuffix = ".gz"
  else:
    myOpen = open
    myMode = "w"
    mySuffix = ""
  csvfile = myOpen(fname + ".csv"  + mySuffix, myMode, newline='')
  jsnfile = myOpen(fname + ".json" + mySuffix, myMode)
  head = True
  for c in customerIDs:
    profile = fake.profile()
    profile['ID'] = c
    print(json.dumps(profile, cls=CustomJsonEncoder), file=jsnfile)
    if head:
      head = False
      fieldnames = profile.keys()
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
      writer.writeheader()
    writer.writerow(profile)
  csvfile.close()
  jsnfile.close()
  return

def generateDeposits(customerIDs, bankIDs, num=10, fname="deposits", mean=100, std=20, cash=0.10, zip=False):
  if zip:
    myOpen = gzip.open
    myMode = "wt"
    mySuffix = ".gz"
  else:
    myOpen = open
    myMode = "w"
    mySuffix = ""
  csvfile = myOpen(fname + ".csv"  + mySuffix, myMode, newline='')
  jsnfile = myOpen(fname + ".json" + mySuffix, myMode)

  # create random transactions between customers (for bank deposits) and cash deposits
  head = True
  for i in range(num):
    # spin the roulette
    luck = random.random()
    isBank = True if luck > cash else False
    numCustomers = 2 if isBank else 1
    customers = random.sample(customerIDs, numCustomers) # returns 1 or 2 customers
    banks     = random.sample(bankIDs, numCustomers) # returns 1 or 2 banks
    deposit = round(random.gauss(mean, std),2)
    timestamp = fake.date_time_between_dates(datetime_start=(datetime.today() - timedelta(days=1)).replace(hour=1, minute=0, second=0, microsecond=0), datetime_end=(datetime.today() - timedelta(days=1)).replace(hour=23, minute=30, second=0, microsecond=0), tzinfo=None)
    record = {
      "timestamp":      timestamp,
      "type":           "bankxfer" if isBank else "cashdepo",
      "amount":         deposit,
      "to_customer":    customers[0],
      "to_bank":        banks[0],
      "to_account":     fake.iban(),
      "from_customer":  customers[1] if isBank else None,
      "from_bank":      banks[1] if isBank else None,
      "from_account":   fake.iban() if isBank else None,
    }
    # print("{} {} {} {} {} {:0.2f} {}\n{}".format(i,luck,isBank,numCustomers,customers,deposit, timestamp,json.dumps(record, cls=CustomJsonEncoder)))
    print(json.dumps(record, cls=CustomJsonEncoder), file=jsnfile)
    if head:
      head = False
      fieldnames = record.keys()
      writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
      writer.writeheader()
    writer.writerow(record)
  csvfile.close()
  jsnfile.close()
  return

def str2bool(v):
  if isinstance(v, bool):
    return v
  if v.lower() in ('yes', 'true', 't', 'y', '1'):
    return True
  elif v.lower() in ('no', 'false', 'f', 'n', '0'):
    return False
  else:
    raise argparse.ArgumentTypeError('Boolean value expected.')


def main():
  args = getArgs()
  print(args)

  start = timer()
  start_time = datetime.now()

  customerIDs = genCustomerIDs(num=args.customers)
  bankIDs     = genBankIDs(num=args.banks)
  writeCustomers(customerIDs, fname=args.fcustomer, zip=args.gzip)
  generateDeposits(customerIDs, bankIDs, num=args.deposits, fname=args.fdeposits, mean=args.amount, std=args.std, cash=args.cash, zip=args.gzip)

  end = timer()
  time_elapsed = datetime.now() - start_time
  print('per record Time (hh:mm:ss.ms) {}'.format(
    timedelta(seconds=end - start) / args.customers))
  print(
    'Clock Time (hh:mm:ss.ms) {} for {} records'.format(time_elapsed, args.customers))


if __name__ == '__main__':
  main()

