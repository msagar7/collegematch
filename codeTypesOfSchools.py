import processdata
import math
from geopy.geocoders import Nominatim

def main():
	weight = {'SAT': 0.007714621651275505, 'ACT': 0.8492448175411861, 'LOCALE': 45.81526523980948, 'CTH': 209.5608309891332, 'CCSIZSET': 99.067590755, 'MAJOR': 201.93980400000004, 'INCOME': 1.0023234242453565}
	collegeData = processdata.createDataDictionary('dataset.csv')
	greeting()
	
	while(True):
		print()
		input("Press enter to start... ")
		print()
		userInput, types = getUserInput()
		# types = {"Target":5,"Reach":5}
		# userInput = {"SAT": 1420, "ACT": 29, "LOCALE": 2, "LOCATION": "Tampa, FL", "CTH": "NO", "CCSIZSET": "MEDIUM", "MAJOR": "ENG", "INCOME": "NPT45_", "TUITION": 100000}

		#print(types)
		distances = {}
		
		geolocator = Nominatim(user_agent = "CollegeMatch")
		loc = geolocator.geocode(userInput["LOCATION"])
		lat = loc.latitude
		lon = loc.longitude


		for ty in types:
			distances = {}
			for cid, cdata in collegeData.items():
				dist = 0
				count = 0
				if cdata["SAT_AVG_ALL"] is None and cdata["ACTCMMID"] is None:
					dist += 1000

				for k, v in userInput.items():

					if v == "N/A" or v == "n/a": continue

					if k == "SAT" or k == "ACT":
						newScore = getUpdatedScore(k,v,ty)
						res_dist, res_count = sat_act(k, newScore, cdata, weight)
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

				if count > 4:
					dist = dist / count
					distances[cid] = dist
					#print(str(cid) + " " + str(collegeData[cid]["INSTNM"]) + ": " + str(dist))

			result = sorted(distances.items(), reverse=False, key=lambda kv: kv[1])
			N = min(types[ty],len(result))
			print()
			print("------" + str(ty)+ " Schools------")
			for i in range(N):
				print(str(i + 1) + ") " + collegeData[result[i][0]]["INSTNM"])# + ": " + str(result[i][1]))
			print("----------------------------------")

def getUpdatedScore(test, score, ty):
	if score == 'N/A' or score == 'n/a':
		return score

	if(test == "SAT"):
		if(ty == "Target"):
			return score
		elif(ty == "Reach"):
			return min(1.1*score,1600) 
		elif(ty == "Safety"):
			return max(.9*score,400)
	elif(test == "ACT"):
		if(ty == "Target"):
			return score
		elif(ty == "Reach"):
			return min(1.1*score,36) 
		elif(ty == "Safety"):
			return max(.9*score ,12)

def greeting():
	print()
	print('Hello and welcome to CollegeMatch! This AI will use your stats and preferences to suggest different schools you can apply to.')
	print('Note these are only suggestions! These are schools you can do more research on to get a better idea of where you may want to apply.')
	print('##########################################################################')
	#print()

def getUserInput():
	userInput = {}
	
	safety = -1
	while(safety < 0):
		safety = input("How many safety schools would you like: ")
		if(safety.isnumeric()):
			safety = int(safety)
		else:
			safety = -1

	target = -1
	while(target < 0):
		target = input("How many target schools would you like: ")
		if(target.isnumeric()):
			target = int(target)
		else:
			target = -1


	reach = -1
	while(reach < 0):
		reach = input("How many reach schools would you like: ")
		if(reach.isnumeric()):
			reach = int(reach)
		else:
			reach = -1

	
	typesOfSchools = {"Safety":safety, "Target":target,"Reach":reach}


	
	#Feature 1: SAT score
	sat_score = -1
	while(sat_score <= 400 or sat_score > 1600):
		sat_score = input('What is your SAT out of 1600? (N/A if did not take) : ')
		if(sat_score == 'n/a' or sat_score == 'N/A'):
			sat_score = 'N/A'
			break
		elif sat_score.isnumeric():
			sat_score = int(sat_score)
		else:
			sat_score = -1 #default to -1 to catch non-numeric inputs


	userInput["SAT"] = sat_score
	
	#Feature 2: ACT score
	act_score = -1
	while(act_score < 12 or act_score > 36):
		act_score = input('What is your ACT out of 36? (N/A if did not take) : ')
		if(act_score == 'n/a' or act_score == 'N/A'):
			act_score = 'N/A'
			break
		elif act_score.isnumeric():
			act_score = int(act_score)
		else:
			act_score = -1 #default to -1 to catch non-numeric inputs

	userInput["ACT"] = act_score

	#Feature 3: Locale Type
	locale = 'not a locale'
	possibleLocales = ['city','suburb','town','rural' ,'n/a' ]
	while(locale not in possibleLocales):
		locale = input('What is your locale preference? (city, suburb, town, rural, n/a): ').lower()

	locale = getLocaleCode(locale)
	userInput["LOCALE"] = locale

	#Feature 4: User Location
	location = input('What is your home location? (please enter as City, State): ')
	userInput["LOCATION"] = location

	#Feature 5: Close to Home?
	cth = None
	while(cth not in ['YES','NO', 'N/A']):
		cth = input('Do you want to be close to home? (yes, no, n/a): ').upper()

	userInput["CTH"] = cth

	#Feature 6: size of school
	possibleSizes = ['SMALL', 'MEDIUM', 'LARGE']
	size = None
	while(size not in possibleSizes):
		size = input('What size school do you prefer? (small, medium, large): ').upper()

	userInput["CCSIZSET"] = size

	#Feature 7: major 
	possibleMajors = ['engineering','natural sciences','business','social sciences','humanities','undecided']
	major = 'none'
	while(major not in possibleMajors):
		major = input('What do you want to study? (engineering, natural sciences, business, social sciences, humanities, undecided): ').lower()

	major = getMajorCode(major)
	userInput["MAJOR"] = major

	#TODO: Decide if we want to add the financial parameters
	print(userInput)
	return userInput, typesOfSchools


def getMajorCode(major):
	majorMap = {'engineering': "ENG", 'natural sciences': "NAT SCI", 'social sciences': "SOC SCI",'business': "BUS", 'humanities': "HUM", 'undecided': "UNDEC"}
	return majorMap[major]

def getLocaleCode(locale):
	localeMap = {'city': 1, 'suburb': 2, 'town': 3, 'rural': 4, 'n/a': 5}
	return localeMap[locale]

def sat_act(k, v, cdata, weight):
	key = None
	if k == "SAT":
		key = "SAT_AVG_ALL"
	elif k == "ACT":
		key = "ACTCMMID"

	res_dist = 0
	res_count = 0

	if v == "N/A" or v == "n/a":
		return res_dist, res_count

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