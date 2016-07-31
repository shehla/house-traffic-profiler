import matplotlib
matplotlib.use('Agg')
import datetime
import pylab as pl
import time
import sys

from googlemaps.route_store import RouteStore
import plotter
import utils

traffic_models = ['pessimistic', 'best_guess', 'optimistic']


class TimeProfiler(object):
    def __init__(self):
        self.route_store = RouteStore()

    def fetch_profile(self, end_time=time.time(), duration=12*60.0*60.0):
        fig = None
        route_store = RouteStore()
        route = {
            #'route_id': 'umairs_place|broadcom',
            #'route_id': 'home|yelp',
            'route_id': 'yelp|home',
            #'route_id': 'omer|broadcom',
            'from': '3255 Vittori Loop, Dublin',
            'to': '190 Mathilda Ave, Sunnyvale',
        }
        recs=route_store.get_time_profile(
            #{'route_id': 'broadcom|umairs_place'},
            route,
            end_time=end_time,
            duration=duration,
        )
        x=[]
        y=[]
        y_o = []
        y_p = []
        for r in recs:
            x.append(float(r['epoch']))
            d = datetime.datetime.fromtimestamp(r['epoch'])
            day_hour = '{0}/{1}/{2} {3}'.format(d.month, d.day, d.year, d.hour)
            y.append({
                'traffic_time': float(r['info']['best_guess']),
                'epoch': r['epoch'],
                'date': day_hour,
            })
            y_p.append({
                'traffic_time': float(r['info']['pessimistic']),
                'epoch': r['epoch'],
                'date': day_hour,
            })
            y_o.append({
                'traffic_time': float(r['info']['optimistic']),
                'epoch': r['epoch'],
                'date': day_hour,
            })

        y = utils.sort_list(y, 'epoch')

        #fig, graph = plotter.plot_stock_qty(y_p, 'traffic_time', fig=fig, line_type='-', show_xticks=False)
        fig, graph = plotter.plot_stock_qty(y, 'traffic_time', fig=fig, line_type='-', show_xticks=True)
        #fig, graph = plotter.plot_stock_qty(y_o, 'traffic_time', fig=fig, line_type='-', show_xticks=True)
        start_time = min([r['epoch'] for r in y_p])
        max_traffic_time = max([r['traffic_time'] for r in y])
        addr_str = 'From:{0}  ==>  To:{1}'.format(route['from'], route['to'])
        graph.text(start_time, max_traffic_time * 1.10, addr_str, fontsize=15)
        pl.ylabel('Time in traffic (mins)')
        pl.ylim([0, max_traffic_time * 1.05])
        pl.legend(traffic_models, loc='lower left')
        pl.savefig('image.png', dpi=400)

if __name__ == '__main__':
    tp = TimeProfiler()
    tp.fetch_profile(end_time=time.time(), duration=float(sys.argv[1]) * 3600.0)
