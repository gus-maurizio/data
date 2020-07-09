import random, csv
from datetime import timedelta, datetime
from faker import Faker
from faker.providers import person
from faker.providers import internet
from faker.providers import ssn
from faker.providers import address
from faker.providers import job
from faker.providers import date_time

from timeit import default_timer as timer
import json

fake = Faker()
fake.add_provider(person)
fake.add_provider(internet)
fake.add_provider(ssn)
fake.add_provider(address)
fake.add_provider(job)
fake.add_provider(date_time)

def first_name_and_gender():
    g = 'M' if random.randint(0,1) == 0 else 'F'
    n = fake.first_name_male() if g=='M' else fake.first_name_female()
    return {'gender':g,'first_name':n}

def birth_and_start_date():
    sd = fake.date_between(start_date="-20y", end_date="now")
    delta = timedelta(days=365*random.randint(18,40))
    bd = sd-delta

    return {'birth_date':bd.strftime('%m/%d/%Y'), 'start_date': sd.strftime('%m/%d/%Y')}

def birth_and_start_date_on_windows():
    bd = datetime(1960, 1, 1) + timedelta(seconds=random.randint(0,1261600000)) #40 year time delta
    earliest_start_date = bd + timedelta(seconds=random.randint(0,567720000)) #earliest start date is 18 years after birth
    latest_start_date = datetime.now()

    delta = latest_start_date-earliest_start_date
    delta_in_seconds = delta.days*24*60*60+delta.seconds
    random_second = random.randint(0,delta_in_seconds)
    return {'birth_date':bd.strftime('%m/%d/%Y'), 'start_date': (bd+timedelta(seconds=random_second)).strftime('%m/%d/%Y')}

def title_office_org():
    #generate a map of real office to fake office
    offices = ['New York','Austin','Seattle','Chicago']
    #codify the hierarchical structure
    allowed_orgs_per_office = {'New York':['Sales'],'Austin':['Devops','Platform','Product','Internal Tools'],'Chicago':['Devops'], 'Seattle':['Internal Tools','Product']}
    allowed_titles_per_org = {
        'Devops':['Engineer','Senior Engineer','Manager'],
        'Sales':['Associate'],
        'Platform':['Engineer'],
        'Product':['Manager','VP'],
        'Internal Tools':['Engineer','Senior Engineer','VP','Manager']
    }

    office = random.choice(offices)
    org = random.choice(allowed_orgs_per_office[office])
    title = random.choice(allowed_titles_per_org[org])
    return {'office':office, 'title':title,'org': org}

def salary_and_bonus():
    salary = round(random.randint(90000,120000)/1000)*1000
    bonus_ratio = random.uniform(0.15,0.2)
    bonus = round(salary*bonus_ratio/500)*500
    return {'salary':salary,'bonus':bonus}

def title_office_org_salary_bonus():
    position = title_office_org()
    title_and_salary_range = {'Engineer':[90,120],'Senior Engineer':[110,140],'Manager':[130,150],'Associate':[60,80],'VP':[150,250]}
    salary_range = title_and_salary_range[position['title']]

    salary = round(random.randint(1000*salary_range[0],1000*salary_range[1])/1000)*1000
    bonus_ratio = random.uniform(0.15,0.2)
    bonus = round(salary*bonus_ratio/500)*500
    position.update({'salary':salary,'bonus':bonus})
    return position

d = dict()
d['first_name_and_gender'] = first_name_and_gender
d['last_name'] = lambda: {'last_name':fake.last_name()}
d['personal_email'] = lambda: {'email':fake.email()}
d['ssn'] = lambda: {'ssn':fake.ssn()}
d['birth_and_start_date'] = birth_and_start_date
d['title_office_org_salary_bonus'] = title_office_org_salary_bonus
d['accrued_holidays']  = lambda: {'accrued_holiday':random.randint(0,20)}
d['transaction_value'] = lambda: {'transaction_value':random.randint(1,20000)}

numRows = 1000
#f = open('fakedata.json', 'w')
csvfile = open('fakedata.csv', 'w', newline='')
head = True
start = timer()
start_time = datetime.now() 

for _ in range(numRows):
    row = {key: val for k in d.keys() for key,val in d[k]().items()}
    if head:
        head = False
        fieldnames = row.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
    # print(json.dumps(row))
    writer.writerow(row)

end = timer()
time_elapsed = datetime.now() - start_time 
csvfile.close()
print('per record Time (hh:mm:ss.ms) {}'.format(timedelta(seconds=end-start)/numRows))
print('Clock Time (hh:mm:ss.ms) {} for {} records'.format(time_elapsed,numRows))
