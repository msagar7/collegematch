import processdata
import randusers
import math
from geopy.geocoders import Nominatim

weight = {"SAT": .01, "ACT": 1.0, "LOCALE": 50, "CTH": 200, "CCSIZSET": 100, "MAJOR": 200, "INCOME": 1}
#weight = {'SAT': 0.009787287515343421, 'ACT': 0.9604039004039601, 'LOCALE': 51.44812060200938, 'CTH': 201.89902019798015, 'CCSIZSET': 100, 'MAJOR': 196.02, 'INCOME': 1}
#weight = {'SAT': 0.008404180271866266, 'ACT': 0.867964254213015, 'LOCALE': 46.93768379696052, 'CTH': 195.80448577866323, 'CCSIZSET': 100, 'MAJOR': 197.98020000000002, 'INCOME': 1}
#weight = {'SAT': 0.007001362042126126, 'ACT': 0.8165942439463155, 'LOCALE': 41.562757811114324, 'CTH': 195.80448577866323, 'CCSIZSET': 99.067590755, 'MAJOR': 197.98020000000002, 'INCOME': 1.0023234242453564}
#weight = {'SAT': 0.007714621651275505, 'ACT': 0.8492448175411861, 'LOCALE': 45.81526523980948, 'CTH': 199.5608309891332, 'CCSIZSET': 99.067590755, 'MAJOR': 201.93980400000004, 'INCOME': 1.0023234242453565}

def main():
	print("YOU ARE ABOUT TO TRAIN THE COLLEGE MATCH ALGORITHM")
	print("INITIAL WEIGHTS: " + str(weight))

	x_train = randusers.generateRandomUsers(50)

	collegeData = processdata.createDataDictionary('dataset.csv')

	f = open("weightsFinal05.txt","a+")
	f2 = open("metricFinal05.txt", "a+")

	for num, userInput in enumerate(x_train):
		print("Training Example #" + str(num))
		print(userInput)

		distances = {}
		importantFeatures = {}

		#weight = {"SAT": 1, "ACT": 5, "LOCALE": 100, "CTH_YES": 1, "CTH_NO": 1000, "CCSIZSET": 1, "MAJOR": 100, "INCOME": 1}
		
		geolocator = Nominatim()
		loc = geolocator.geocode(userInput["LOCATION"])
		if loc == None:
			continue
		lat = loc.latitude
		lon = loc.longitude

		for cid, cdata in collegeData.items():

			imp1_cat = "NONE"
			imp1_dist = float("inf")
			imp2_cat = "NONE"
			imp2_dist = float("inf")

			dist = 0
			count = 0
			if cdata["SAT_AVG_ALL"] is None and cdata["ACTCMMID"] is None:
				dist += 1000

			for k, v in userInput.items():
				if v == "N/A": continue

				if k == "SAT" or k == "ACT":
					res_dist, res_count = sat_act(k, v, cdata, weight)
					imp1_cat, imp1_dist, imp2_cat, imp2_dist = updateImp(k, res_dist, res_count, imp1_cat, imp1_dist, imp2_cat, imp2_dist)
					dist += res_dist
					count += res_count

				if k == "CCSIZSET":
					res_dist, res_count = size(k, v, cdata, weight)
					imp1_cat, imp1_dist, imp2_cat, imp2_dist = updateImp(k, res_dist, res_count, imp1_cat, imp1_dist, imp2_cat, imp2_dist)
					dist += res_dist
					count += res_count

				if k == "LOCALE":
					res_dist, res_count = locale(k, v, cdata, weight)
					imp1_cat, imp1_dist, imp2_cat, imp2_dist = updateImp(k, res_dist, res_count, imp1_cat, imp1_dist, imp2_cat, imp2_dist)
					dist += res_dist
					count += res_count

				if k == "LOCATION":
					res_dist, res_count = location(lat, lon, cdata, userInput, weight)
					imp1_cat, imp1_dist, imp2_cat, imp2_dist = updateImp("CTH", res_dist, res_count, imp1_cat, imp1_dist, imp2_cat, imp2_dist)
					dist += res_dist
					count += res_count

				if k == "LONGITUDE" or k == "CTH":
					continue

				if k == "MAJOR":
					res_dist, res_count = major(k, v, cdata, weight)
					imp1_cat, imp1_dist, imp2_cat, imp2_dist = updateImp(k, res_dist, res_count, imp1_cat, imp1_dist, imp2_cat, imp2_dist)
					dist += res_dist
					count += res_count

				if k == "INCOME":
					res_dist, res_count = income_tuition(k, v, cdata, userInput, weight)
					#imp1_cat, imp1_dist, imp2_cat, imp2_dist = update(k, res_dist, res_count, imp1_cat, imp1_dist, imp2_cat, imp2_dist)
					dist += res_dist
					count += res_count

			if count > 4:
				dist = dist / count
				distances[cid] = dist
				importantFeatures[cid] = [imp1_cat, imp2_cat]
				#print(str(cid) + " " + str(collegeData[cid]["INSTNM"]) + ": " + str(dist))

		result = sorted(distances.items(), reverse=False, key=lambda kv: kv[1])

		outputResults(collegeData, result)

		feedback = getFeedback(f2)

		updateWeights(feedback, importantFeatures, result, f, num+1)

	f.close()
	f2.close()

def updateWeights(feedback, importantFeatures, result, f, num):
	N = 10
	epsilon = .05
	for j in range(N):
		fb = feedback[j]
		impFeatures = importantFeatures[result[j][0]]
		# print(impFeatures)
		# print(fb)
		if fb == 'y':
			weight[impFeatures[0]] *= (1.0 - epsilon)
			weight[impFeatures[1]] *= (1.0 - epsilon)
		elif fb == 'n':
			weight[impFeatures[0]] *= (1.0 + epsilon)
			weight[impFeatures[1]] *= (1.0 + epsilon)

	f.write("Example " + str(num) + ") New Weights: " + str(weight) + "\n")
	print("Updated Weights: " + str(weight))


def outputResults(collegeData, result):
	N = 10
	print("------Top 10 College Matches------")
	for i in range(N):
		cdata = collegeData[result[i][0]]

		loc = cdata["LOCALE"]
		locale = "N/A"
		if loc // 10 == 1:
			locale = "City"
		elif loc // 10 == 2:
			locale = "Suburb"
		elif loc // 10 == 3:
			locale = "Town"
		elif loc // 10 == 4:
			locale = "Rural"

		ccsize = cdata["CCSIZSET"]
		size = "N/A"
		sizes = [[1,6,7,8,2,9,10,11],[3,12,13,14],[4,5,15,16,17],[-2,0,18]]
		for j, arr in enumerate(sizes):
			if ccsize in arr:
				if j == 0:
					size = "Small"
				elif j == 1:
					size = "Medium"
				elif j == 2:
					size = "Large"

		sat_avg = str(cdata["SAT_AVG_ALL"])
		act_avg = str(cdata["ACTCMMID"])

		print(str(i + 1) + ") " + cdata["INSTNM"] + "\nLocale: " + locale + "\tSize: " + size + "\tACT: " + act_avg + "\tSAT: " + sat_avg)# + ": " + str(result[i][1]))
		#print("Top Features: " + str(importantFeatures[result[i][0]]))
	print("----------------------------------")

def getFeedback(f2):
	fb1 = input('1) y/n: ')
	fb2 = input('2) y/n: ')
	fb3 = input('3) y/n: ')
	fb4 = input('4) y/n: ')
	fb5 = input('5) y/n: ')
	fb6 = input('6) y/n: ')
	fb7 = input('7) y/n: ')
	fb8 = input('8) y/n: ')
	fb9 = input('9) y/n: ')
	fb10 = input('10) y/n: ')

	arr = [fb1, fb2, fb3, fb4, fb5, fb6, fb7, fb8, fb9, fb10]
	count = 0
	for i in range(10):
		if arr[i] == 'y':
			count += 1
	f2.write(str(count) + "\n")

	return arr

def updateImp(k, res_dist, res_count, imp1_cat, imp1_dist, imp2_cat, imp2_dist):
	if res_count == 0:
		return imp1_cat, imp1_dist, imp2_cat, imp2_dist
	if imp1_dist == float("inf"):
		# imp1_cat = k
		# imp1_dist = res_dist
		return k, res_dist, imp2_cat, imp2_dist
	if imp2_dist == float("inf"):
		# imp2_cat = k
		# imp2_dist = res_dist
		return imp1_cat, imp1_dist, k, res_dist
	if res_dist < imp1_dist:
		# imp2_dist = imp1_dist
		# imp2_cat = imp1_cat
		# imp1_dist = res_dist
		# imp1_cat = k
		return k, res_dist, imp1_cat, imp1_dist
	elif res_dist < imp2_dist:
		# imp2_dist = res_dist
		# imp2_cat = k
		return imp1_cat, imp1_dist, k, res_dist
	else:
		return imp1_cat, imp1_dist, imp2_cat, imp2_dist

def sat_act(k, v, cdata, weight):
	key = None
	if k == "SAT":
		key = "SAT_AVG_ALL"
	elif k == "ACT":
		key = "ACTCMMID"

	res_dist = 0
	res_count = 0

	if cdata[key] is not None:
		score = int(cdata[key])
		if score > int(v):
			res_dist = 2 * weight[k] * (v - score)**2
		else:
			res_dist = weight[k] * (v - score)**2
		res_count = 2
	return res_dist, res_count

def locale(k, v, cdata, weight):
	res_dist = 0
	res_count = 0
	if cdata[k] is not None and v != 5:
		col_locale = int(cdata[k])
		col_type = col_locale // 10
		#col_size = col_locale % 10
		req_type = v
		#req_size = v % 10
		res_dist = weight[k] * (col_type - req_type)**2 #+ (col_size - req_size)**2)
		res_count = 1
	return res_dist, res_count

def size(k, v, cdata, weight):
	res_dist = 0
	res_count = 0
	sizes = [[1,6,7,8,2,9,10,11],[3,12,13,14],[4,5,15,16,17],[-2,0,18]]

	if cdata[k] is not None:
		req_size = None
		if v == "SMALL": 
			req_size = 1
		elif v == "MEDIUM":
			req_size = 2
		else:
			req_size = 3 

		col_ccsizset = int(cdata[k])
		col_size = None

		for i, arr in enumerate(sizes):
			if col_ccsizset in arr:
				col_size = i + 1

		if col_size != req_size and col_size != 4:
			res_dist = abs(col_size - req_size) * weight[k]
			res_count = 1

	return res_dist, res_count

def major(k, v, cdata, weight):
	res_dist = 0
	res_count = 0

	majors = {
		"ENG": ["PCIP14", "PCIP15", "PCIP11", "PCIP27", "PCIP41"],
		"NAT SCI": ["PCIP01", "PCIP26", "PCIP27", "PCIP40", "PCIP41", "PCIP51"],
		"SOC SCI": ["PCIP09", "PCIP10", "PCIP22", "PCIP42", "PCIP45"],
		"HUM": ["PCIP04", "PCIP23", "PCIP24", "PCIP05", "PCIP13", "PCIP16", "PCIP38", "PCIP50", "PCIP54"],
		"BUS": ["PCIP52"]
	}

	if v != "UNDEC":
		arr = majors[v]
		perc = 0
		for elem in arr:
			if cdata[elem] is not None:
				perc += float(cdata[elem])

		if perc < .03:
			res_dist = weight[k]
		elif perc < .15:
			res_dist = .5 * weight[k]
		else:
			res_dist = .2 * weight[k]
		res_count = 1

	return res_dist, res_count

def income_tuition(k, v, cdata, userInput, weight):
	res_dist = 0
	res_count = 0

	endings = ["PUB", "PRIV"]
	avg_cost = 0
	for ending in endings:
		column = v + ending
		if cdata[column] is not None:
			avg_cost = float(cdata[column])
	if avg_cost != 0 and avg_cost < userInput["TUITION"]:
		res_dist = 0
		res_count = 1
		#print(dist)
	elif avg_cost != 0:
		res_dist = weight[k] * (avg_cost - userInput["TUITION"])**2
		res_count = 1

	return res_dist, res_count

def location(lat, lon, cdata, userInput, weight):
	res_dist = 0
	res_count = 0

	if cdata["LATITUDE"] is not None and cdata["LONGITUDE"] is not None:
		cth = "CTH_" + userInput["CTH"]
		col_lat = float(cdata["LATITUDE"])
		col_lon = float(cdata["LONGITUDE"])
		col_dist = (col_lat - lat)**2 + (col_lon - lon)**2

		if cth == "CTH_YES":
			if col_dist < 150:
				res_dist = .1 * weight["CTH"]
			elif col_dist < 700:
				res_dist = .9 * weight["CTH"]
			else:
				res_dist = weight["CTH"]
			res_count = 1
			#dist += weight[cth] * col_dist
			#print(dist)
		elif cth == "CTH_NO":
			if col_dist < 150:
				res_dist = weight["CTH"]
			elif col_dist < 700:
				res_dist = .9 * weight["CTH"]
			else:
				res_dist = .1 * weight["CTH"]
			res_count = 1

	return res_dist, res_count

if __name__ == "__main__":
	main()