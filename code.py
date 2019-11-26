import processdata
import math
from geopy.geocoders import Nominatim

def main():
	collegeData = processdata.createDataDictionary('dataset.csv')
	getUserInput()
	#userInput = {"SAT": 1520, "ACT": 35, "LOCALE": 22, "LATITUDE":40, "LONGITUDE":-75, "CTH": "NO", "CCSIZSET": "LARGE", "MAJOR": "ENG", "INCOME": "NPT41_", "TUITION": 10000}
	userInput = {"SAT": 1400, "ACT": 28, "LOCALE": 2, "LOCATION": "The Woodlands, TX", "CTH": "YES", "CCSIZSET": "MEDIUM", "MAJOR": "ENG", "INCOME": "NPT45_", "TUITION": 100000}
	distances = {}
	
	#weight = {"SAT": 1, "ACT": 5, "LOCALE": 100, "CTH_YES": 1, "CTH_NO": 1000, "CCSIZSET": 1, "MAJOR": 100, "INCOME": 1}
	weight = {"SAT": .01, "ACT": 1, "LOCALE": 50, "CTH_YES": 200, "CTH_NO": 200, "CCSIZSET": 100, "MAJOR": 200, "INCOME": 1}
	
	
	geolocator = Nominatim()
	loc = geolocator.geocode(userInput["LOCATION"])
	lat = loc.latitude
	lon = loc.longitude
	# megac = 0
	for cid, cdata in collegeData.items():
		#if count > 10: continue
		#print("CID: " + str(cid))
		dist = 0
		count = 0
		if cdata["SAT_AVG_ALL"] is None and cdata["ACTCMMID"] is None:
			dist += 1000

		for k, v in userInput.items():
			if v == "N/A": continue

			if k == "SAT" or k == "ACT":
				res_dist, res_count = sat_act(k, v, cdata, weight)
				dist += res_dist
				count += res_count

			if k == "CCSIZSET":
				res_dist, res_count = size(k, v, cdata, weight)
				dist += res_dist
				count += res_count

			if k == "LOCALE":
				res_dist, res_count = locale(k, v, cdata, weight)
				dist += res_dist
				count += res_count

			if k == "LOCATION":
				res_dist, res_count = location(lat, lon, cdata, userInput, weight)
				dist += res_dist
				count += res_count

			if k == "LONGITUDE" or k == "CTH":
				continue

			if k == "MAJOR":
				res_dist, res_count = major(k, v, cdata, weight)
				dist += res_dist
				count += res_count

			if k == "INCOME":
				res_dist, res_count = income_tuition(k, v, cdata, userInput, weight)
				dist += res_dist
				count += res_count

			# if k == "LATITUDE":
			# 	if cdata["LATITUDE"] is not None or cdata["LONGITUDE"] is not None:
			# 		lat = v
			# 		lon = userInput["LONGITUDE"]
			# 		cth = "CTH_" + userInput["CTH"]
			# 		col_lat = float(cdata["LATITUDE"])
			# 		col_lon = float(cdata["LONGITUDE"])
			# 		col_dist = (col_lat - lat)**2 + (col_lon - lon)**2
			# 		#col_dist = max(math.log(col_dist,2),1)
			# 		#print(col_dist)
			# 		if cth == "CTH_YES":
			# 			if col_dist < 200:
			# 				dist += .2 * weight[cth]
			# 			elif col_dist < 700:
			# 				dist += .5 * weight[cth]
			# 			else:
			# 				dist += weight[cth]
			# 			count += 1
			# 			#dist += weight[cth] * col_dist
			# 			#print(dist)
			# 		elif cth == "CTH_NO":
			# 			if col_dist < 200:
			# 				dist += weight[cth]
			# 			elif col_dist < 700:
			# 				dist += .5 * weight[cth]
			# 			else:
			# 				dist += .2 * weight[cth]
			# 			count += 1
						#dist += weight[cth] / col_dist
						#print(dist)
				#else:
					#dist += 1000
					#print(dist)

			# if cid == 134130:
			# 	print(str(k))
			# 	print(str(dist))
			# 	print(str(count))
		# if cid == 134130:
		# 	print("WTF")
		# 	print(str(dist))
		# 	print(str(count))
		if count > 4:
			dist = dist / count
			distances[cid] = dist
			#print(str(cid) + " " + str(collegeData[cid]["INSTNM"]) + ": " + str(dist))

	result = sorted(distances.items(), reverse=False, key=lambda kv: kv[1])
	N = 10
	print("------Top 10 College Matches------")
	for i in range(N):
		#print(result[i][0])
		print(str(i + 1) + ") " + collegeData[result[i][0]]["INSTNM"])# + ": " + str(result[i][1]))
	print("----------------------------------")

def getUserInput():
	userInput = {}
	#userInput = {"SAT": 1520, "ACT": 35, "LOCALE": 2, "LOCATION": "Chicago,IL", "CTH": "NO", "CCSIZSET": "MEDIUM", "MAJOR": "ENG", "INCOME": "NPT45_", "TUITION": 100000}
	sat_score = -1
	while(sat_score < 0 or sat_score > 1600):
		sat_score = input('What is your SAT out of 1600? (N/A if did not take) : ')
		if(sat_score == 'n/a' or 'N/A'):
			break
		else:
			sat_score = int(sat_score)

	userInput["SAT"] = sat_score
	
	act_score = -1
	while(act_score < 0 or act_score > 36):
		act_score = input('What is your ACT out of 1600? (N/A if did not take) : ')
		if(act_score == 'n/a' or 'N/A'):
			break
		else:
			act_score = int(act_score)

	userInput["ACT"] = act_score

	locale = 'not a locale'
	possibleLocales = ['urban','rural','suburban', 'n/a' ]
	while(locale not in possibleLocales):
		locale = input('What is your locale preference? (urban, rural, suburban, n/a): ').lower()


	#TODO: transform locale to a number
	userInput["LOCALE"] = locale

	location = input('What is your home location? (please enter as City, State): ')
	userInput["LOCATION"] = location

	cth = None
	while(cth not in ['YES','NO']):
		cth = input('Do you want to be close to home? (enter yes or no): ').upper()

	userInput["CTH"] = cth

	possibleSizes = ['SMALL', 'MEDIUM', 'LARGE']
	size = None
	while(size not in possibleSizes):
		size = input('What size school do you prefer? (small, medium, large): ').upper()

	userInput["CCSIZSET"] = size

	possibleMajors = ['engineering','natural sciences','business','social sciences','humanities','undecided']
	major = 'none'
	while(major not in possibleMajors):
		major = input('What do you want to study? (engineering, natural sciences, business, social sciences, humanities, undecided): ').lower()

	major = getMajorCode(major)
	userInput["MAJOR"] = major

	#TODO: Decide if we want to add the financial parameters
	print(userInput)
	return userInput


def getMajorCode(major):
	majorMap = {'engineering': "ENG", 'natural sciences': "NAT SCI", 'social sciences': "SOC SCI",'business': "BUS", 'humanities': "HUM", 'undecided': "UNDEC"}
	return majorMap[major]


def sat_act(k, v, cdata, weight):
	key = None
	if k == "SAT":
		key = "SAT_AVG_ALL"
	elif k == "ACT":
		key = "ACTCMMID"

	res_dist = 0
	res_count = 0

	if cdata[key] is not None:
		score = float(cdata[key])
		if score > v:
			res_dist = 2 * weight[k] * (v - score)**2
		else:
			res_dist = weight[k] * (v - score)**2
		res_count = 2
	return res_dist, res_count

def locale(k, v, cdata, weight):
	res_dist = 0
	res_count = 0
	if cdata[k] is not None:
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
				res_dist = .1 * weight[cth]
			elif col_dist < 700:
				res_dist = .9 * weight[cth]
			else:
				res_dist = weight[cth]
			res_count = 1
			#dist += weight[cth] * col_dist
			#print(dist)
		elif cth == "CTH_NO":
			if col_dist < 150:
				res_dist = weight[cth]
			elif col_dist < 700:
				res_dist = .9 * weight[cth]
			else:
				res_dist = .1 * weight[cth]
			res_count = 1

	return res_dist, res_count

if __name__ == "__main__":
	main()