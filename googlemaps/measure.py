import re
import sys
import json
import time

from googlemaps.route_store import RouteStore
from googlemaps.delay_controller import DelayController


traffic_models = ['optimistic', 'best_guess', 'pessimistic']


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
                rec = {
                    'route_id': route['route_id'],
                    'time': time.time(),
                    'current_delay': delay_controllers[route['route_id']].current_delay,
                    'info': resp,
                }
                route_mgr.report('travel_time_profiles', rec)
        time.sleep(1.0)
