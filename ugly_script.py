import requests, datetime
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()
@sched.scheduled_job('interval', seconds=10)
def timed_job():
	print("ruuun")
	total_bikes = 4000
	file = open("available_bikes_timeseries_domingo02.txt","a+")
	date = datetime.datetime.now()
	response = requests.get("https://apitransporte.buenosaires.gob.ar/ecobici/gbfs/stationStatus?client_id=85a38f2e925347ea9ca8fcbeb2d959be&client_secret=D5A11b275Bc347a598f14074299e7e73")
	response = response.json()
	data = response['data']
	stations = data['stations']
	date = datetime.datetime.now()
	available_bikes_total = 0
	disabled_bikes_total = 0
	for station in stations:
		available_bikes = station['num_bikes_available']
		disabled_bikes = station['num_bikes_disabled']
		available_bikes_total += available_bikes
		disabled_bikes_total += disabled_bikes
	bikes_in_use = total_bikes - disabled_bikes_total - available_bikes_total - 1580
	file.write (str(date.date()) + ','+ str(date.time()) + ',' + str(bikes_in_use))
	file.write('\n')
	file.close() 
	print("bikes in use: " + str(bikes_in_use))
	print (str(date.date()) + ','+ str(date.time()) + ',' + str(bikes_in_use))
sched.start()