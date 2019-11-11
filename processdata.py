import csv
from collections import defaultdict

# Loads the csv file of college data into a dictionary
# params: 
# 	- filename: name of csv file containing the dataset
# return:
#	- dictionary:
#		- key: college UNITID defined by DOE
#		- value: dictionary containing different data
#				 points of each college (eg. city, 
#				 % undergraduate males)
def createDataDictionary(filename):
	column_names = []
	master = defaultdict(dict)
	header = True
	with open(filename) as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		for row in reader:
			if header: 
				column_names = row
				header = False
			else:
				college_id = int(row[0])
				for i in range(1, len(row)):
					datapoint = None 
					if row[i].isnumeric(): # numerical data
						datapoint = float(row[i])
					elif row[i] != "NULL":
						datapoint = row[i]
					master[college_id][column_names[i]] = datapoint
	return master

if __name__ == "__main__":
	master = createDataDictionary('dataset.csv')
	print(master[101116]['ZIP'])

