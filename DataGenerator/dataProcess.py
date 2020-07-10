#!/usr/bin/env python3

import random, csv, json, argparse, uuid, os, gzip

from decimal import *
from bloom_filter import BloomFilter
from decimal import Decimal
from timeit import default_timer as timer
from datetime import timedelta, datetime, date

# getcontext().prec = 2


class CustomJsonEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return float(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return super(CustomJsonEncoder, self).default(obj)

def getArgs():
  parser = argparse.ArgumentParser(description='Process test data.')
  parser.add_argument('-fc', '--fcustomer', type=str, default="customer", help='filename (no extension)')
  parser.add_argument('-fd', '--fdeposits', type=str, default="deposits", help='filename (no extension)')
  parser.add_argument('-z',  '--gzip',      type=str2bool, nargs='?',const=True, default=False,help='Activate gzip.')
  args = parser.parse_args()
  return args

def processDeposits(fname="deposits", zip=False):
  if zip:
    myOpen = gzip.open
    myMode = "rt"
    mySuffix = ".gz"
  else:
    myOpen = open
    myMode = "r"
    mySuffix = ""

  numRecords = 0
  numBank = 0
  numCash = 0
  to_customers = set()
  to_banks = set()
  from_customers = set()
  from_banks = set()

  csvfile = myOpen(fname + ".csv"  + mySuffix, myMode, newline='')
  jsnfile = myOpen(fname + ".json" + mySuffix, myMode)

  bankDeposit = Decimal('0.00')
  cashDeposit = Decimal('0.00')
  totDeposits = Decimal('0.00')
  reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
  for row in reader:
    amt = Decimal(row['amount'])
    numRecords  += 1
    totDeposits += amt
    to_customers.add(row['to_customer'])
    to_banks.add(row['to_bank'])
    if row['type'] == 'bankxfer':
      bankDeposit = bankDeposit + amt
      numBank  += 1
      from_customers.add(row['from_customer'])
      from_banks.add(row['from_bank'])
    if row['type'] == 'cashdepo':
      cashDeposit = cashDeposit + amt
      numCash  += 1
    if numRecords % 50000 == 0:
      print('>>>>> {:10,d} {:20,.2f} {:10,d} {:20,.2f} {:10,d} {:20,.2f}'.format(numRecords,totDeposits,numBank,bankDeposit,numCash,cashDeposit))

  csvfile.close()
  jsnfile.close()
  print('##### {:10,d} {:20,.2f} {:10,d} {:20,.2f} {:10,d} {:20,.2f}'.format(numRecords,totDeposits,numBank,bankDeposit,numCash,cashDeposit))
  print('##### unique TO customers {:10,d} banks {:10,d} FROM customers {:10,d} banks {:10,d} '.format(len(to_customers),len(to_banks),len(from_customers),len(from_banks)))
  return numRecords

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

  numRec = processDeposits(fname=args.fdeposits, zip=args.gzip)

  end = timer()
  time_elapsed = datetime.now() - start_time
  print('per record Time (hh:mm:ss.ms) {}'.format(
    timedelta(seconds=end - start) / numRec))
  print(
    'Clock Time (hh:mm:ss.ms) {} for {} records'.format(time_elapsed, numRec))


if __name__ == '__main__':
  main()

