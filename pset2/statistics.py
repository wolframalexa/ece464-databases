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
soup = bs(union_data)

# find industries & numbers
sep = soup.find("p", string="INDUSTRY")

industries = sep.find_all_next("p", ["sub1", "sub2"])

# remove tags
for i in range(len(industries)):
	industries[i] = industries[i].get_text()

# TODO: only pick datavalues related to sub1 and sub2 industry tags
numbers = sep.find_all_next("span", "datavalue")

# remove tags and turn into floats
for i in range(0, len(numbers)):
	num = numbers[i].get_text()
	numbers[i] = float(num.replace(',',''))

# write to file for further parsing later
for i in range(0, len(industries)):
	out = industries[i] + " " + str(numbers[i*10:i*10+9]) + "\n"
	f.write(out)

#################
# RACE & GENDER #
#################
# open race and gender makeup page
#browser.get("https://www.bls.gov/cps/cpsaat18.htm")

# read table
#rows = browser.find_elements_by_xpath("html/body/div/table/tbody/tr")
#print(rows)



f.close()
