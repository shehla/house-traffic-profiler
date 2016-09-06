from googlemaps.route_store import RouteStore


if __name__ == '__main__':
    route_store = RouteStore()
    routes = route_store.get_routes()
    for cur_route in routes:
        print('******************************')
        print('route_id:{}\nfrom:{}\nto:{}\n'.format(
            cur_route['route_id'],
            cur_route['from'],
            cur_route['to'],
        ))
