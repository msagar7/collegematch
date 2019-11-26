import random
import csv
from collections import defaultdict
import processdata
from geopy.geocoders import Nominatim
import statistics

def getRandomElement(vals, pdf):
	assert len(vals) == len(pdf)
	cdf = pdf
	for i in range(1, len(cdf)):
		cdf[i] += cdf[i - 1]
	prob = random.random()

	print(cdf)
	for i in range(len(cdf)):
		if prob <= cdf[i]: return vals[i]



# Loads the csv file of college data into a dictionary
# params: 
# 	- filename: name of csv file containing the dataset
# return:
#	- dictionary:
#		- key: college UNITID defined by DOE
#		- value: dictionary containing different data
#				 points of each college (eg. city, 
#				 % undergraduate males)
def generateRandomUsers():
	random.seed(420)
	collegeData = processdata.createDataDictionary('dataset.csv')
	
	# Determine distributions for the user input features using college info
	sat_scores, act_scores, locales = [], [], []
	for cid, cdata in collegeData.items():
		if cdata["SAT_AVG_ALL"] is not None: sat_scores.append(cdata["SAT_AVG_ALL"])
		if cdata["ACTCMMID"] is not None: act_scores.append(cdata["ACTCMMID"])
	sat_mean = statistics.mean(sat_scores)
	sat_std = statistics.stdev(sat_scores)
	act_mean = statistics.mean(act_scores)
	act_std = statistics.stdev(act_scores)

	locale_vals = [1, 2, 3, 4, 5]
	locale_pdf  = [.225, .225, .225, .225, .1]

	cth_vals = ["YES", "NO", "N/A"]
	cth_pdf  = [.4, .4, .2]

	size_vals = ["SMALL", "MEDIUM", "LARGE", "N/A"]
	size_pdf  = [0.3, 0.3, 0.3, 0.1]

	major_vals = ["ENG", "NAT SCI", "SOC SCI", "HUM", "BUS", "UNDEC"]
	major_pdf  = [1/6, 1/6, 1/6, 1/6, 1/6, 1/6]

	income_vals = ["NPT41_", "NPT42_", "NPT43_", "NPT44_", "NPT45_"]
	income_pdf  = [0.2, 0.2, 0.2, 0.2, 0.2]

	locations =   ["Bald Head, IL",
				"Sullivans Landing, LA",
				"Wickware, YK",
				"Burdickville, BC",
				"Saint Hilaire Village, NU",
				"Chestnut Hill, WA",
				"Hamilton Square, OR",
				"Longdale, NM",
				"Melbourne Village, ON",
				"Dobyns, MD",
				"Morley, OR",
				"Wayport, CO",
				"Morgan Manor, SK",
				"Lima Center, FL",
				"Nutt, VT",
				"Hartland, TN",
				"Mcmullin, CA",
				"New Windsor, OH",
				"Dunlay, OH",
				"West Denmark, NV",
				"Edmore, YK",
				"Mabank, MD",
				"Urgon, NM",
				"Clay Sink, LA",
				"Victor, MI",
				"Errol, WI",
				"Bacotville, CA",
				"Furnace Creek, MI",
				"Hunting, MO",
				"Berlin, DE",
				"Bel Air Estates, WY",
				"Ecum Secum, NV",
				"Mann, CO",
				"Unco, WA",
				"Wilna, WI",
				"Cantwell, CT",
				"Sonora, OR",
				"Glen Aubin, NJ",
				"Emerson, SK",
				"Oats, OR",
				"Packs Harbour, NY",
				"Lewis Creek, AL",
				"Cold Spring, NH",
				"Buskirk, MN",
				"Toneyville, GA",
				"Brookover Estates, MI",
				"Beatrice, ND",
				"Pole Tavern, MS",
				"Cedar Grove, MS",
				"Garden City, WA",
				"Lavina, ID",
				"Sewellsville, SC",
				"Remo, PA",
				"Cross Mountain, WY",
				"Seven Harbors, MT",
				"Chelsea, KS",
				"Pactolus, MB",
				"Woodside Crossing, YK",
				"Mount Jordan Addition, NC",
				"Mount Comfort, HI",
				"Mountain View, TX",
				"East Cromwell, SD",
				"Wertz Crossroads, NU",
				"Munjoy Hill, PE",
				"Dunns Fort, AK",
				"Post Town, NU",
				"Wetsel, DE",
				"Mount Airy Springs, HI",
				"Old Mines, NY",
				"Piattsville, NC",
				"Nymph, MS",
				"Tejon, MN",
				"Keystone, YK",
				"Creekwood, ME",
				"Wallace Crossroads, TX",
				"Ellis Place, CA",
				"Lafayette, CO",
				"Tynan, ON",
				"Lynnview, UT",
				"Cairo, WY",
				"Ariel, TN",
				"Parkview, WA",
				"Eastern View, SC",
				"Arriola, TX",
				"Kellogg, WI",
				"Van Dorn Corner, MN",
				"Dew Drop, OH",
				"Hobbie Farm, SC",
				"Cataldo, NH",
				"Diamond, NY",
				"Chalkley, AL",
				"North Star, MN",
				"Hardwick, AL"]

	users = []
	for user_num in range(100):
		user_info = dict()
		sat_data = random.normalvariate(sat_mean, sat_std)
		sat_data = 100 if sat_data < 0 else sat_data
		sat_data = 1600 if sat_data > 1600 else sat_data
		user_info["SAT"] = round(sat_data)

		act_data = random.normalvariate(act_mean, act_std)
		act_data = 5 if act_data < 0 else act_data
		act_data = 36 if act_data > 36 else act_data
		user_info["ACT"] = round(act_data)

		# user_info["LOCALE"] = getRandomElement(locale_vals, locale_pdf)
		# user_info["CTH"] = getRandomElement(cth_vals, cth_pdf)
		# user_info["SIZE"] = getRandomElement(size_vals, size_pdf)
		user_info["MAJOR"] = getRandomElement(major_vals, major_pdf)
		# user_info["INCOME"] = getRandomElement(income_vals, income_pdf)
		# user_info["TUITION"] = 100000
		# user_info["LOCATION"] = random.choice(locations)

		users.append(user_info)
	return users


if __name__ == "__main__":
	users = generateRandomUsers()
	print(users)

