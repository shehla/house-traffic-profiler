import matplotlib
matplotlib.use('Agg')
import datetime
from matplotlib.dates import date2num
import numpy as np
import pylab as pl

import stock_common


def scatter_values_with_dates(buy_values, buy_dates, color, marker_type):
    dates =  stock_common.convert_str_to_datetime(buy_dates)
    buy_dates = [date2num(dd) for dd in dates]
    pl.scatter(buy_dates, buy_values, marker=marker_type, s=40, c=color, edgecolor=color)

# stock_data is a list of price recs which has volume, price, date(string) etc
def plot_stock_qty(stock_data, qty_name, fig=None, show_xticks=True, line_type='-', is_scatter=False, color='b', size=1):
    if len(stock_data[0]['date'].split()) == 2:
        is_hourly = True
    else:
        is_hourly = False

    if is_hourly:
        epoch_times = [stock_common.get_epoch_time(r['date'], is_hourly=True) for r in stock_data]
    else:
        epoch_times = [stock_common.get_epoch_time(r['date']) for r in stock_data]
    prices = [r[qty_name] for r in stock_data]
    if fig == None:
        fig = pl.figure(figsize=(12, 6))
    graph = fig.add_subplot(111)
    #graph.plot(epoch_times, prices)
    plot_numbers_against_dates(stock_data, fig, qty_name, line_type, is_scatter, color, size)
    if show_xticks:
        plot_x_ticks_with_dates(graph, stock_data, False)
    graph.grid(True)
    return fig, graph

def plot_bar(x_labels, y_vals, fig, c, width=0.35):
    graph = fig.add_subplot(111)
    ind = np.arange(len(y_vals))
    graph.bar(ind+width, y_vals, width=0.35, color=c)
    graph.set_xticks(ind+0.35)
    graph.set_xticklabels(x_labels)
    graph.set_xlabel('Year')
    graph.set_ylabel('Annual return (%)')
    return graph

def plot_x_ticks_with_dates(graph, current_value, do_all):
    if not do_all:
        LABEL_DIFF = int(len(current_value) / 8)
    else:
        LABEL_DIFF = 1
    dates_strings = [dd['date'] for dd in current_value[0::LABEL_DIFF]]
    #dates = stock_common.convert_str_to_datetime(dates_strings)
    #dates_num = [date2num(dd) for dd in dates]
    #dates_num = [int(dd['epoch']) for dd in current_value[0::LABEL_DIFF]]
    dates_num = [int(dd['epoch']) for dd in current_value]
    dates_num = range(min(dates_num), max(dates_num), int((max(dates_num) - min(dates_num)) / 8.0))
    print('=======>', dates_num, int(max(dates_num) - min(dates_num) / 8.0))
    graph.set_xticks(dates_num)
    #dates = stock_common.convert_str_to_datetime(dates_strings)
    dates = [datetime.datetime.fromtimestamp(r) for r in dates_num]
    graph.set_xticklabels(['/'.join('/'.join(str(r).split()[0].split('-')).split('/')[1:])+' '+str(r).split()[1].split(':')[0]+':00' for r in dates], fontsize=8)
    return graph

def plot_numbers_against_numbers(x_vals, y_vals, fig):
    graph = fig.add_subplot(111)
    graph.plot(x_vals, y_vals)
    return graph

# Takes a dict having key/values for amount and date. Plots
# amounts against dates
def plot_numbers_against_dates(current_value, fig, property_name='amount', line_type='-', is_scatter=False, color='b', size=1):
    graph = fig.add_subplot(111)
    #dates = [dd['date'] for dd in current_value]
    #dates = stock_common.convert_str_to_datetime(dates)
    #dates_num = [date2num(dd) for dd in dates]
    dates_num = [r['epoch'] for r in current_value]
    if is_scatter:
        graph.scatter(dates_num, [v[property_name] for v in current_value], linestyle=line_type, linewidth=2, color=color, s=size)
    else:
        graph.plot(dates_num, [v[property_name] for v in current_value], linestyle=line_type, linewidth=2)
    return graph
