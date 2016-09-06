import argparse
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import pylab as pl
from pytz import timezone
import time
import sys

from googlemaps.route_store import RouteStore
import plotter
import utils

#traffic_models = ['pessimistic', 'best_guess', 'optimistic']
traffic_models = ['best_guess']


class TimeProfiler(object):
    def __init__(self):
        self.route_store = RouteStore()

    def fetch_profile(self, route_id, start_time, end_time):
        fig = None
        route_store = RouteStore()
        route = {
            #'route_id': 'umairs_place|broadcom',
            #'route_id': 'home|yelp',
            #'route_id': 'yelp|home',
            'route_id': route_id,
            #'route_id': 'omer|broadcom',
        }
        routes = route_store.get_routes()
        for cur_route in routes:
            if cur_route['route_id'] == route['route_id']:
                route = cur_route
        recs=route_store.get_time_profile(
            #{'route_id': 'broadcom|umairs_place'},
            route,
            start_time=start_time,
            end_time=end_time,
        )
        x=[]
        y=[]
        for r in recs:
            x.append(float(r['epoch']))
            d = datetime.fromtimestamp(r['epoch'])
            day_hour = '{0}/{1}/{2} {3}'.format(d.month, d.day, d.year, d.hour)
            try:
                y.append({
                    'traffic_time': float(r['info']['best_guess']),
                    'epoch': r['epoch'],
                    'date': day_hour,
                })
            except KeyError:
                continue

        y = utils.sort_list(y, 'epoch')

        #fig, graph = plotter.plot_stock_qty(y_p, 'traffic_time', fig=fig, line_type='-', show_xticks=False)
        fig, graph = plotter.plot_stock_qty(y, 'traffic_time', fig=fig, line_type='-', show_xticks=True)
        #fig, graph = plotter.plot_stock_qty(y_o, 'traffic_time', fig=fig, line_type='-', show_xticks=True)
        start_time = min([r['epoch'] for r in y])
        max_traffic_time = max([r['traffic_time'] for r in y])
        addr_str = 'From:{0}  ==>  To:{1}'.format(route['from'], route['to'])
        graph.text(start_time, max_traffic_time * 1.10, addr_str, fontsize=15)
        pl.ylabel('Time in traffic (mins)')
        pl.ylim([0, max_traffic_time * 1.05])
        pl.legend(traffic_models, loc='lower left')
        pl.savefig('image.png', dpi=400)

def convert_to_epoch_pst(d):
    datetime_obj_pacific = timezone('US/Pacific').localize(d)
    return float(datetime_obj_pacific.strftime('%s'))

def valid_date(s):
    try:
        return datetime.strptime(s, "%m/%d/%Y %H:%M")
    except ValueError:
        return datetime.strptime(s, "%m/%d/%Y")
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def parse_command_line(args):
    """ Parses supplied args for configuration settings

    :param args: argument list to parse
    :return: populated argument namespace
    """

    cli_parser = argparse.ArgumentParser(description="Car driving times tool",
                                         conflict_handler='error')
    cli_parser.add_argument("-r", "--route-id",
                            nargs='?',
                            required=True,
                            help="Specify a Route id")
    cli_parser.add_argument("-s", "--start-time",
                            nargs='?',
                            required=True,
                            type=valid_date,
                            help="Start time format is MM/DD/YYYY HH:MM")
    cli_parser.add_argument("-e", "--end-time",
                            nargs='?',
                            required=True,
                            type=valid_date,
                            help="End time format is MM/DD/YYYY HH:MM")
    return cli_parser.parse_args(args)

if __name__ == '__main__':
    tp = TimeProfiler()
    cli_args = parse_command_line(sys.argv[1:])
    start_time = convert_to_epoch_pst(cli_args.start_time)
    end_time = convert_to_epoch_pst(cli_args.end_time)
    print('route:{} start:{} end:{} duration:{}'.format(
        cli_args.route_id,
        start_time,
        end_time,
        (end_time - start_time) / 3600.0,
    ))
    tp.fetch_profile(cli_args.route_id, start_time, end_time)
