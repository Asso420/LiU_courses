from __future__ import division
from math import radians, cos, sin, asin, sqrt, exp
from datetime import datetime
from pyspark import SparkContext

sc = SparkContext(appName="lab_kernel")

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

h_distance = 100 
h_date     = 14 
h_time     = 2 

# h_distance = 1000 
# h_date     = 30
# h_time     = 2 

a    = 58.4274  # linköpings latitude
b    = 14.826   # linköpings longitude
target_date = "2013-07-04"  # the date for which we want to find the nearby stations and their temperature readings

stations = sc.textFile("hdfs:///user/x_ahmso/BDA/input/stations.csv")
temps    = sc.textFile("hdfs:///user/x_ahmso/BDA/input/temperature-readings.csv")
#temps    = sc.textFile("hdfs:///user/x_ahmso/BDA/input/temperature-readings-small.csv")
# Your code here
lines_stations = stations.map(lambda line: line.split(";"))
lines_temps    = temps.map(lambda line: line.split(";"))

structured_stations = lines_stations.map(lambda x: (x[0], (float(x[3]), float(x[4])))) # (stationID, lat, lon)
structured_temps    = lines_temps.map(lambda x: (x[0], x[1], x[2], float(x[3]))) # (stationID, date, time, temperature)

stations_dict = sc.broadcast(structured_stations.collectAsMap()) # broadcast the station information to all workers, so that we can compute distances in the following steps

valid_temps = structured_temps.filter(lambda x: x[1] <= target_date)
valid_temps.cache()

results = []
for time in ["24:00:00", "22:00:00", "20:00:00", "18:00:00", "16:00:00",
             "14:00:00", "12:00:00", "10:00:00", "08:00:00", "06:00:00", "04:00:00"]:

    target_hour = int(time.split(":")[0])
    current_valid_temps = valid_temps.filter(lambda x: False if (x[1] == target_date and x[2] > time) else True
    )

    def compute_weight(reading):
        stationID, date, time, temperature = reading

        data_lot, data_lon = stations_dict.value[stationID]
        dist_km = haversine(b, a, data_lon, data_lot)

        diff_days = (abs((datetime.strptime(target_date, "%Y-%m-%d") - datetime.strptime(date, "%Y-%m-%d")).days))
        dist_date = min(diff_days, 365 - diff_days)

        diff_hours = (abs(int(target_hour) - int(time.split(":")[0])))
        dist_time = min(diff_hours, 24 - diff_hours)

        kernel_distance = exp(-(dist_km**2) / (h_distance**2))
        kernel_date = exp(-(dist_date**2) / (h_date**2))
        kernel_time = exp(-(dist_time**2) / (h_time**2))

        total_weight_sum = kernel_distance + kernel_date + kernel_time 
        #total_weight_product = kernel_distance * kernel_date * kernel_time
        
        return (total_weight_sum, total_weight_sum*temperature)
        #return (total_weight_product, total_weight_product*temperature)

    mapped_rdd = current_valid_temps.map(compute_weight)

    weighted_sum = mapped_rdd.reduce(lambda x, y: (x[0] + y[0], x[1] + y[1]))

    sum_weights = weighted_sum[0]
    sum_weighted_temps = weighted_sum[1]

    estimated_temp = sum_weighted_temps / sum_weights

    results.append(f"Estimated temperature for {time}: {estimated_temp}")
results_rdd = sc.parallelize(results)
results_rdd.saveAsTextFile("hdfs:///user/x_ahmso/BDA/output")