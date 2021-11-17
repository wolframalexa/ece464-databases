# this script scrapes statistics from several sources to populate my ethics database

import requests
import math
from bs4 import BeautifulSoup as bs


####################
# UNION MEMBERSHIP #
####################

f = open("union_table.txt", "w")

# read table
union_data = requests.get(url = 'https://www.bls.gov/news.release/union2.t03.htm').text

# parse: turn results into table with industry and numbers
soup = bs(union_data, "html.parser")

# find industries & numbers
sep = soup.find("p", string="INDUSTRY")

industries_u = sep.find_all_next("p", ["sub0", "sub1", "sub2","sub3"])

# remove tags
for i in range(len(industries_u)):
	industries_u[i] = industries_u[i].get_text()

numbers = sep.find_all_next("span", "datavalue")

# remove tags and turn into floats
for i in range(0, len(numbers)):
	num = numbers[i].get_text()
	numbers[i] = float(num.replace(',',''))

# write to file and format for insertion into db
union_data = []
for i in range(0, len(industries_u)):
	out = industries_u[i] + " " + str(numbers[i*10:(i+1)*10]) + "\n"
	union_data.append(numbers[i*10:(i+1)*10])
	f.write(out)
f.close()

#################
# RACE & GENDER #
#################
# open file
f = open("race_gender_table.txt", "w")

# open race and gender makeup page
race_gender_data = requests.get(url = "https://www.bls.gov/cps/cpsaat18.htm").text

# read table: data is all from 2020
rg_soup = bs(race_gender_data, 'html.parser')
industries_rg = rg_soup.find_all("p", ["sub0", "sub1", "sub2", "sub3"])

numbers_rg = rg_soup.find_all("span", "datavalue")

# remove tags, turn into floats, turn into NaNs where applicable
for i in range(0, len(numbers_rg)):
	num = numbers_rg[i].get_text()
	num = num.replace("-","NaN")
	num = float(num.replace(',',''))
	if math.isnan(num):
		num = None
	numbers_rg[i] = num

for i in range(0, len(industries_rg)):
	industries_rg[i] = industries_rg[i].get_text()

# remove text tags and write to file
rg_data = []

for i in range(0, len(industries_rg)):
	out = industries_rg[i] + " " + str(numbers_rg[i*6:(i+1)*6]) + "\n"
	rg_data.append(numbers_rg[i*6:(i+1)*6])
	f.write(out)

##########
# SALARY #
##########

f = open("salary_table.txt", "w")
salary_data = requests.get(url = "https://www.bls.gov/oes/current/oes_nat.htm").text

salary_soup = bs(salary_data, 'html.parser')

occupations = salary_soup.find_all("table", "display")
salary_data = []
temp = occupations[i].find_all("tr")

# TODO: fix this so I get a nice table out of it
for i in range(0, temp):
	for j in range(0, len(temp)):
		temp[j] = temp[j].get_text()
	salary_data.append(temp)
#	f.write(temp)
print("salary_data length", len(salary_data))
f.close()


#################
# CREATE TABLES #
#################
from sqlalchemy import func, create_engine, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, Float
import uuid

engine = create_engine('mysql+pymysql://alexa:Hello123%21%40%23@localhost:3306/pset2')
Session = sessionmaker(bind=engine)
session = Session()

meta = MetaData()

union_industries = Table(
	'union_industries', meta,
	Column('iid', Integer, primary_key = True),
	Column('name', String(100)),
	Column('tot_employees_19', Integer),
	Column('union_members_19', Integer),
	Column('union_members_percent_19', Float),
	Column('union_rep_19', Integer),
	Column('union_rep_percent_19', Float),

	Column('tot_employees_20', Integer),
	Column('union_members_20', Integer),
	Column('union_members_percent_20', Float),
	Column('union_rep_20', Integer),
	Column('union_rep_percent_20', Float),
)

#union_industries.create(engine, checkfirst=True) # don't recreate table if already exists

#for i in range(0, len(industries_u)):
# insert item into table
#	stmt = insert(union_industries).values(iid=i+50, name = industries_u[i], tot_employees_19 = union_data[i][0], union_members_19 = union_data[i][1], union_members_percent_19 = union_data[i][2], union_rep_19 = union_data[i][3], union_rep_percent_19 = union_data[i][4], tot_employees_20 = union_data[i][5], union_members_20 = union_data[i][6], union_members_percent_20 = union_data[i][7], union_rep_20 = union_data[i][8], union_rep_percent_20 = union_data[i][9])
#
#	conn = engine.connect()
#	result = conn.execute(stmt)
#	session.commit()

race_gender_industries = Table(
	'race_gender_industries', meta,
	Column('iid', Integer, primary_key=True),
	Column('name', String(200)),
	Column('tot_employees', Integer),
	Column('perc_women', Float, nullable=True),
	Column('perc_white', Float, nullable=True),
	Column('perc_black', Float, nullable=True),
	Column('perc_asian', Float, nullable=True),
	Column('perc_hisp_latino', Float, nullable=True),
)
#race_gender_industries.create(engine, checkfirst=True)

#for i in range(0, len(industries_rg)):
#	stmt = insert(race_gender_industries).values(iid= 100+i, name=industries_rg[i], tot_employees=rg_data[i][0], perc_women=rg_data[i][1], perc_white=rg_data[i][2], perc_black=rg_data[i][3], perc_asian=rg_data[i][4], perc_hisp_latino=rg_data[i][5])
#
#	conn = engine.connect()
#	result = conn.execute(stmt)
#	session.commit()


salary_info = Table(
	'salary_info', meta,
	Column('oid', String(7), primary_key=True),
	Column('name', String(60)),
	Column('level', String(10)),
	Column('tot_employees', Integer),
	Column('rse', Float),
	Column('emp_per_1000_jobs', Float),
	Column('med_hourly_wage', Float),
	Column('mean_hourly_wage', Float)
)

salary_info.create(engine, checkfirst=True)

for i in range(0, len(salary_data)):
	print(salary_data[i])
	print(i)
#	stmt = insert(salary_info).values(oid = salary_data[i][0], name=salary_data[i][1], level=salary_data[i][2], tot_employees=salary_data[i][3], rse=salary_data[i][4], emp_per_1000_jobs = salary_data[i][5], med_hourly_wage=salary_data[i][6], mean_hourly_wage = salary_data[i][7])

#	conn = engine.connect()
#	result = conn.execute(stmt)
#	session.commit()






# Sample queries
