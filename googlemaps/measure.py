from datetime import datetime
from termcolor import colored
import re
import sys
import json
import time

from googlemaps.route_store import RouteStore
from googlemaps.delay_controller import DelayController


traffic_models = ['optimistic', 'pessimistic', 'best_guess']


if __name__ == '__main__':
    route_mgr = RouteStore()
    routes = route_mgr.get_routes()
    delay_controllers = {}
    while True:
        for route in routes:
            if route['route_id'] not in delay_controllers:
                delay_controllers[route['route_id']] = DelayController(route)
            resp = delay_controllers[route['route_id']].check_and_run()
            if resp:
                print colored('\n\nTime:{0}'.format(str(datetime.today()).split('.')[0]), 'blue')
                rec = {
                    'route_id': route['route_id'],
                    'time': time.time(),
                    'current_delay': delay_controllers[route['route_id']].current_delay,
                    'info': json.dumps(resp),
                }
                route_mgr.report('travel_time_profiles', rec)
        time.sleep(2.0)
