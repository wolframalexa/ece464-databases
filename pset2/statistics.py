# this script scrapes statistics from several sources to populate my ethics database

import requests
import time
from bs4 import BeautifulSoup as bs


f = open("union_table.txt", "w")

####################
# UNION MEMBERSHIP #
####################

# read table
union_data = requests.get(url = 'https://www.bls.gov/news.release/union2.t03.htm').text

# parse: turn results into table with industry and numbers
soup = bs(union_data, "html.parser")

# find industries & numbers
sep = soup.find("p", string="INDUSTRY")

industries = sep.find_all_next("p", ["sub0", "sub1", "sub2","sub3"])

# remove tags
for i in range(len(industries)):
	industries[i] = industries[i].get_text()

numbers = sep.find_all_next("span", "datavalue")

# not sure if this will work, could also remove manually
#industries.find_all_parents().find_all_siblings("span", "datavalue")

# remove tags and turn into floats
for i in range(0, len(numbers)):
	num = numbers[i].get_text()
	numbers[i] = float(num.replace(',',''))

# write to file for further parsing later
for i in range(0, len(industries)):
	out = industries[i] + " " + str(numbers[i*10:i*10+9]) + "\n"
	f.write(out)
f.close()

#################
# RACE & GENDER #
#################
# open file
f = open("race_gender_table.txt", "w")

# open race and gender makeup page
race_gender_data = requests.get(url = "https://www.bls.gov/cps/cpsaat18.htm").text

# read table
rg_soup = bs(race_gender_data, 'html.parser')
industries_rg = rg_soup.find_all("p", ["sub0", "sub1", "sub2", "sub3"])

numbers_rg = rg_soup.find_all("span", "datavalue")

# remove tags, turn into floats, turn into NaNs where applicable
for i in range(0, len(numbers_rg)):
	num = numbers_rg[i].get_text()
	num = num.replace("-","NaN")
	numbers_rg[i] = float(num.replace(',',''))

for i in range(0, len(industries_rg)):
	industries_rg[i] = industries_rg[i].get_text()

# remove text tags and write to file
for i in range(0, len(industries_rg)):
	out = industries_rg[i] + " " + str(numbers_rg[i*6:i*6+5]) + "\n"
	f.write(out)

##########
# SALARY #
##########

f = open("salary_table.txt", "w")
salary_data = requests.get(url = "https://www.bls.gov/oes/current/oes_nat.htm").text

salary_soup = bs(salary_data, 'html.parser')

occupations = salary_soup.find_all("tr")
salary_data = []
for i in range(0, len(occupations)):
	temp = occupations[i].find_all("td")
	for j in range(0, len(temp)):
		temp[j] = temp[j].get_text()
	salary_data.append(temp)

print(salary_data)

f.close()
