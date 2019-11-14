from geopy.geocoders import Nominatim

def hoe():
	geolocator = Nominatim()
	loc = geolocator.geocode("Houston,TX")
	print(loc.latitude)
	print(loc.longitude)

hoe()