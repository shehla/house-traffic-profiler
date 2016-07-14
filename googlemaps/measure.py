import googlemaps
import re
import sys
import json
from datetime import datetime
import time

from googlemaps.route_store import RouteStore
from googlemaps.delay_controller import DelayController


DELAY = float(sys.argv[1])
gmaps = googlemaps.Client(key='AIzaSyDNIxQQlAu-LzbpCQhvJDMKtPgborYIO7w')
traffic_models = ['optimistic', 'best_guess', 'pessimistic']

def get_time(_from, _to, traffic_model='best_guess'):
	# Request directions via public transit
    now = datetime.now()
    directions_result = gmaps.directions(_from,_to,mode="driving",departure_time=now,traffic_model=traffic_model)
    traffic_time = directions_result[0]['legs'][0]['duration_in_traffic']['text']
    print('model:{0} Time in traffic:{1}'.format(traffic_model, traffic_time))
    s = re.split(" +", traffic_time)
    if 'hour' in s or 'hours' in s:
        total_time = float(s[0]) * 60 + float(s[2])
    else:
        total_time = float(s[0])
    return total_time


if __name__ == '__main__':
    route_mgr = RouteStore()
    routes = route_mgr.get_routes()
    delay_controllers = {}
    while True:
        for route in routes:
            if route['route_id'] not in delay_controllers:
                delay_controllers[route['route_id']] = DelayController(route['route_id'])
            for model in traffic_models:
                time_in_mins = get_time(route['from'], route['to'], model)
                # only use delay for best_guess
                if model == 'best_guess':
                    delay_controllers[route['route_id']].update_queue(time_in_mins)
                rec = {
                    'route_id': route['route_id'],
                    'time': time.time(),
                    'traffic_model': model,
                    'traffic_time': time_in_mins,
                    'current_delay': delay_controllers[route['route_id']].current_delay,
                }

                print(json.dumps(rec))
                route_mgr.report('travel_time_profiles', rec)
        time.sleep(DELAY)
