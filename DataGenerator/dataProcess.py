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
  csvfile = myOpen(fname + ".csv"  + mySuffix, myMode, newline='')
  jsnfile = myOpen(fname + ".json" + mySuffix, myMode)

  bankDeposit = Context().create_decimal('0.00')
  cashDeposit = Context().create_decimal('0.00')
  totDeposits = Context().create_decimal('0.00')
  reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
  for row in reader:
    amt = Decimal(row['amount'])
    numRecords  += 1
    totDeposits += amt
    if row['type'] == 'bankxfer':
      bankDeposit = bankDeposit + amt
    if row['type'] == 'cashdepo':
      cashDeposit = cashDeposit + amt
  csvfile.close()
  jsnfile.close()
  print('{0:20.2f}'.format(totDeposits))
  print('{0:20.2f}'.format(bankDeposit))
  print('{0:20.2f}'.format(cashDeposit))
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

