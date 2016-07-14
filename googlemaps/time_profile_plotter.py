import matplotlib
matplotlib.use('Agg')
import pylab as pl
import time
import sys

from googlemaps.route_store import RouteStore


class TimeProfiler(object):
    def __init__(self):
        self.route_store = RouteStore()

    def fetch_profile(self, end_time=time.time(), duration=6*60.0*60.0):
        route_store = RouteStore()
        recs=route_store.get_time_profile(
            {'route_id': 'umairs_place|broadcom'},
            end_time=end_time,
            duration=6*60.0*60.0,
        )
        x=[]
        y=[]
        for r in recs:
            x.append(float(r['epoch']))
            y.append(float(r['info']['best_guess']))

        pl.plot(x,y)
        pl.ylim([0, max(y)*1.05])
        pl.savefig('image.png')

if __name__ == '__main__':
    tp = TimeProfiler()
    tp.fetch_profile(duration=float(sys.argv[1]) * 3600.0)
