# this script scrapes statistics from several sources to populate my ethics database

import requests
import math
from bs4 import BeautifulSoup as bs

# get data from webpages using scraping

####################
# UNION MEMBERSHIP #
####################
print("Scraping data...")

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

#################
# RACE & GENDER #
#################

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

##########
# SALARY #
##########

salary_data = requests.get(url = "https://www.bls.gov/oes/current/oes_nat.htm").text

salary_soup = bs(salary_data, 'html.parser')

occupations = salary_soup.find("table", {"class": ["display", "sortable_datatable", "fixed-headers", "dataTable", "no-footer"]}) # find main datatable
body = occupations.find("tbody")
data = body.find_all("tr")
salary_data = []

# extract datapoints & clean data of tags
for i in range(0, len(data)):
	tmp = data[i].find_all("td")

	# clean of extraneous characters, handle NULLs
	for j in range(0, len(tmp)):
		value = tmp[j].get_text()
		value = value.replace('$','')
		value = value.replace('%','')
		value = value.replace(',','')
		if (value.count('(') > 0):
			value = None
		tmp[j] = value

	salary_data.append(tmp)

print("Scraping done! Now creating tables")

#################
# CREATE TABLES #
#################

from sqlalchemy import func, create_engine, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, String, MetaData, Float

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

union_industries.create(engine, checkfirst=True) # don't recreate table if already exists
for i in range(0, len(industries_u)):
# insert item into table
	stmt = insert(union_industries).values(iid=i+50, name = industries_u[i], tot_employees_19 = union_data[i][0], union_members_19 = union_data[i][1], union_members_percent_19 = union_data[i][2], union_rep_19 = union_data[i][3], union_rep_percent_19 = union_data[i][4], tot_employees_20 = union_data[i][5], union_members_20 = union_data[i][6], union_members_percent_20 = union_data[i][7], union_rep_20 = union_data[i][8], union_rep_percent_20 = union_data[i][9])

	conn = engine.connect()
	result = conn.execute(stmt)
	session.commit()

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
race_gender_industries.create(engine, checkfirst=True)

for i in range(0, len(industries_rg)):
	stmt = insert(race_gender_industries).values(iid= 100+i, name=industries_rg[i], tot_employees=rg_data[i][0], perc_women=rg_data[i][1], perc_white=rg_data[i][2], perc_black=rg_data[i][3], perc_asian=rg_data[i][4], perc_hisp_latino=rg_data[i][5])

	conn = engine.connect()
	result = conn.execute(stmt)
	session.commit()


salary_info = Table(
	'salary_info', meta,
	Column('oid', String(7), primary_key=True),
	Column('name', String(200)),
	Column('level', String(10)),
	Column('tot_employees', Integer),
	Column('rse', Float),
	Column('emp_per_1000_jobs', Float),
	Column('med_hourly_wage', Float),
	Column('mean_hourly_wage', Float),
	Column('annual_mean_wage', Float),
	Column('rse_mean_wage', Float)
)

salary_info.create(engine, checkfirst=True)

for i in range(0, len(salary_data)):
	tmp = salary_data[i]

	# enforce datatypes, when floats are none
	try:
		num_emp = int(tmp[3])
		rse_emp = float(tmp[4])
		per_1000 = float(tmp[5])
	except:
		num_emp = None
		rse_emp = None
		per_1000 = None

	try:
		med_wage = float(tmp[6])
		mean_wage = float(tmp[7])
	except:
		med_wage = None
		mean_wage = None

	try:
		annual_mean = int(tmp[8])
	except:
		annual_mean = None
	rse_mean = float(tmp[9])

	stmt = insert(salary_info).values(oid = tmp[0], name=tmp[1], level=tmp[2], tot_employees=num_emp, rse=rse_emp, emp_per_1000_jobs = per_1000, med_hourly_wage=med_wage, mean_hourly_wage = mean_wage, annual_mean_wage = annual_mean, rse_mean_wage = rse_mean)

	conn = engine.connect()
	result = conn.execute(stmt)
	session.commit()

print("Tables created. Now running three sample queries. Here are their results:")

##################
# SAMPLE QUERIES #
##################

from sqlalchemy import func

# find the number of occupations with an annual mean salary of over 50k a year
s1 = session.query(func.count(salary_info.c.oid)).filter(salary_info.c.annual_mean_wage >= 50000.0).scalar()
print("Number of occupations with salary >50k:", s1)

# find 10 industries with the most women
s2 = session.query(race_gender_industries.c.name).order_by(race_gender_industries.c.perc_women.desc()).limit(10).all()
print("Industries with the most women:", s2)

# find occupations and industries where union density is growing (percent 2020 members > 2019 members)
s3 = session.query(union_industries.c.name, union_industries.c.union_members_percent_19, union_industries.c.union_members_percent_20).filter(union_industries.c.union_members_percent_19 < union_industries.c.union_members_percent_20).all()
print("Industries where union density grew from 2019 to 2020:", s3)

