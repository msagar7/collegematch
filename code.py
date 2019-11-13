import processdata
import math

def main():
	collegeData = processdata.createDataDictionary('dataset.csv')
	userInput = {"SAT": 1520, "ACT": 35, "LOCALE": 22, "LATITUDE":28, "LONGITUDE":-82, "CTH": "NO", "CCSIZSET": "LARGE", "MAJOR": "ENG", "INCOME": "NPT41_", "TUITION": 10000}
	distances = {}
	endings = ["PUB", "PRIV"]
	#weight = {"SAT": 1, "ACT": 5, "LOCALE": 100, "CTH_YES": 1, "CTH_NO": 1000, "CCSIZSET": 1, "MAJOR": 100, "INCOME": 1}
	weight = {"SAT": .01, "ACT": 1, "LOCALE": 50, "CTH_YES": 150, "CTH_NO": 150, "CCSIZSET": 100, "MAJOR": 200, "INCOME": 1}
	sizes = [[1,6,7,8,2,9,10,11],[3,12,13,14],[4,5,15,16,17],[-2,0,18]]
	majors = {
		"ENG": ["PCIP14", "PCIP15", "PCIP11", "PCIP27", "PCIP41"],
		"NAT SCI": ["PCIP01", "PCIP26", "PCIP27", "PCIP40", "PCIP41", "PCIP51"],
		"SOC SCI": ["PCIP09", "PCIP10", "PCIP22", "PCIP42", "PCIP45"],
		"HUM": ["PCIP04", "PCIP23", "PCIP24", "PCIP05", "PCIP13", "PCIP16", "PCIP38", "PCIP50", "PCIP54"],
		"BUS": ["PCIP52"]
	}
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
				key = None
				if k == "SAT":
					key = "SAT_AVG_ALL"
				elif k == "ACT":
					key = "ACTCMMID"

				if cdata[key] is not None:
					score = float(cdata[key])
					if score > v:
						dist += 2 * weight[k] * (v - score)**2
					else:
						dist += weight[k] * (v - score)**2
					count += 2
				# else:
				# 	punish_count += 1
				# 	if punish_count == 2:
				# 		dist += 1000
					#print(dist)
				#else:
					#dist += 1000
					#print(dist)
			if k == "CCSIZSET":
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
					# if megac < 10:
					# 	print(str(req_size) + " " + str(col_size))
					# 	megac += 1
					if col_size != req_size and col_size != 4:
						dist += abs(col_size - req_size) * weight[k]
						count += 1



			if k == "LOCALE":
				if cdata[k] is not None:
					col_locale = int(cdata[k])
					col_type = col_locale // 10
					#col_size = col_locale % 10
					req_type = v // 10
					#req_size = v % 10
					dist += weight[k] * (col_type - req_type)**2 #+ (col_size - req_size)**2)
					count += 1
					#print(dist)
			if k == "LATITUDE":
				if cdata["LATITUDE"] is not None or cdata["LONGITUDE"] is not None:
					lat = v
					lon = userInput["LONGITUDE"]
					cth = "CTH_" + userInput["CTH"]
					col_lat = float(cdata["LATITUDE"])
					col_lon = float(cdata["LONGITUDE"])
					col_dist = (col_lat - lat)**2 + (col_lon - lon)**2
					#col_dist = max(math.log(col_dist,2),1)
					#print(col_dist)
					if cth == "CTH_YES":
						if col_dist < 200:
							dist += .2 * weight[cth]
						elif col_dist < 700:
							dist += .5 * weight[cth]
						else:
							dist += weight[cth]
						count += 1
						#dist += weight[cth] * col_dist
						#print(dist)
					elif cth == "CTH_NO":
						if col_dist < 200:
							dist += weight[cth]
						elif col_dist < 700:
							dist += .5 * weight[cth]
						else:
							dist += .2 * weight[cth]
						count += 1
						#dist += weight[cth] / col_dist
						#print(dist)
				#else:
					#dist += 1000
					#print(dist)

			if k == "LONGITUDE" or k == "CTH":
				continue

			if k == "MAJOR":
				if v != "UNDEC":
					arr = majors[v]
					perc = 0
					for elem in arr:
						if cdata[elem] is not None:
							perc += float(cdata[elem])

					if perc < .03:
						dist += weight[k]
					elif perc < .15:
						dist += .5 * weight[k]
					else:
						dist += .2 * weight[k]
					count += 1



				# if cdata[v] is not None:
				# 	perc = float(cdata[v])
				# 	count += 1
				# 	if perc < .03:
				# 		dist += weight[k]
				# 	elif perc < .15:
				# 		dist += .5 * weight[k]
				# 	else:
				# 		dist += .2 * weight[k]
					#dist += weight[k] * (1 - float(cdata[v]))
					#print(dist)
				#else:
					#dist += 100
					#print(dist)

			if k == "INCOME":
				avg_cost = 0
				for ending in endings:
					column = v + ending
					if cdata[column] is not None:
						avg_cost = float(cdata[column])
				if avg_cost != 0 and avg_cost < userInput["TUITION"]:
					dist += 0
					count += 1
					#print(dist)
				elif avg_cost != 0:
					dist += weight[k] * (avg_cost - userInput["TUITION"])**2
					count += 1
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
				# print(str(dist))
				# print(str(count))
			dist = dist / count
			distances[cid] = dist
			#print(str(cid) + " " + str(collegeData[cid]["INSTNM"]) + ": " + str(dist))

	result = sorted(distances.items(), reverse=False, key=lambda kv: kv[1])
	N = 10
	for i in range(N):
		#print(result[i][0])
		print(collegeData[result[i][0]]["INSTNM"] + ": " + str(result[i][1]))







if __name__ == "__main__":
	main()