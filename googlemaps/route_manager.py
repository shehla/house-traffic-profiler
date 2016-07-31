from datetime import datetime
from termcolor import colored
import re

import googlemaps

gmaps = googlemaps.Client(key='AIzaSyDNIxQQlAu-LzbpCQhvJDMKtPgborYIO7w')

def get_time(_from, _to, traffic_model='best_guess'):
    # Request directions via public transit
    now = datetime.now()
    try:
        directions_result = gmaps.directions(_from,_to,mode="driving",departure_time=now,traffic_model=traffic_model)
        traffic_time = directions_result[0]['legs'][0]['duration_in_traffic']['text']
    except Exception e:
        print('Nothing found :S {0}'.format(e))
        return None
    if traffic_model == 'best_guess':
        print colored('model:{0} Time in traffic:{1}'.format(traffic_model, traffic_time), 'green')
    else:
        print('model:{0} Time in traffic:{1}'.format(traffic_model, traffic_time))
    s = re.split(" +", traffic_time)
    if 'hour' in s or 'hours' in s:
        total_time = float(s[0]) * 60 + float(s[2])
    else:
        total_time = float(s[0])
    return total_time
