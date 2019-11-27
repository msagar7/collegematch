import random
import csv
from collections import defaultdict
import processdata
from geopy.geocoders import Nominatim
import statistics

def getRealUsers():
	titles = ['TIME', 'ACT', 'SAT', 'LOCATION', 'MAJOR', 'CTH', 'LOCALE', 'SIZE']
	header = True
	users = []
	with open('users.csv') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		for row in reader:
			if header:
				header = False
				continue
			else:
				user_info = dict()
				for i in range(1, 8):
					value = row[i]
					if titles[i] == 'SAT' or titles[i] == 'ACT':
						if value != 'N/A': value = float(value)
					elif titles[i] == 'LOCATION':
						pass
					elif titles[i] == 'MAJOR':
						# ["ENG", "NAT SCI", "SOC SCI", "HUM", "BUS", "UNDEC"]
						if value == 'Engineering': value = 'ENG'
						elif value == 'Natural Sciences': value = 'NAT SCI'
						elif value == 'Social Sciences': value = 'SOC SCI'
						elif value == 'Humanities': value = 'HUM'
						elif value == 'Business': value = "BUS"
						else: value = 'UNDEC'
					elif titles[i] == 'CTH':
						if value == 'Yes': value = 'YES'
						elif value == 'No': value = 'NO'
						elif value == 'Did not care': value = 'N/A'
					elif titles[i] == 'LOCALE':
						# {'city': 1, 'suburb': 2, 'town': 3, 'rural': 4, 'n/a': 5}
						if value == 'City': value = 1
						elif value == 'Suburb': value = 2
						elif value == 'Town': value = 3
						elif value == 'Rural': value = 4
						elif value == 'Did not care': value = 5
					elif titles[i] == 'SIZE':
						if value == 'Small': value = 'SMALL'
						elif value == 'Large': value = 'Large'
						elif value == 'Medium': value = 'Medium'
						elif value == 'Did not care': value = 'N/A'
					user_info[titles[i]] = value
		
				users.append(user_info)
	return users


if __name__ == "__main__":
	users = getRealUsers()
	for user in users:
		print(user)
	print(len(users))

