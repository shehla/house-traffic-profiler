import googlemaps
import sys
import json
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyDNIxQQlAu-LzbpCQhvJDMKtPgborYIO7w')

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions(
    sys.argv[1],
    sys.argv[2],
               #                      "Laurel, CA",
               #                      "Bethany Park, CA",
                                     mode="driving",
                                    departure_time=now,
                                    #traffic_model="optimistic",
                                    #traffic_model="pessimistic",
                                    traffic_model="best_guess",
                                     #departure_time=datetime(2016, 7, 14, 13, 40, 48, 612402)
                                    )
#print(json.dumps(directions_result))
print('Time in traffic:{0}'.format(directions_result[0]['legs'][0]['duration_in_traffic']['text']))
print('Time in regular:{0}'.format(directions_result[0]['legs'][0]['duration']['text']))
