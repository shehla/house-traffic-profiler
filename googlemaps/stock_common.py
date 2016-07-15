import calendar
import json
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import os
import random
import time
import sys


def convert_list_to_dict(recs, col_name):
    new_dict = {}
    for r in recs:
        new_dict[r[col_name]] = r
    return new_dict

def get_last_price(price_recs, today):
    current_day = today
    symbol = price_recs.values()[0]['symbol']
    for x in range(0, -60, -1):
        try:
            return price_recs[current_day]['price']
            current_day = add_days_to_date(today, x)
        except KeyError:
            current_day = add_days_to_date(today, x)
            continue
    print('[stock_common] No closer price for {0} {1}'.format(symbol, today))

def add_months(sourcedate,months):
     month = sourcedate.month - 1 + months
     year = sourcedate.year + month / 12
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
     return datetime.date(year,month,day)

def convert_datetime_to_num(dates):
    dates = [dd['date'] for dd in dates_datetime]
    dates = stock_common.convert_str_to_datetime(dates)
    return [date2num(dd) for dd in dates]

def convert_str_to_datetime(dates_strings, slash_format=True):
    dates = []
    for date_string in dates_strings:
        if not slash_format:
            dates.append(datetime.strptime(date_string, "%d-%m-%Y"))
        else:
            dates.append(datetime.strptime(date_string, "%m/%d/%Y %H"))
    return dates

def find_market_open_day_backward(today):
    return find_market_open_day(today, False)

def find_market_open_day_forward(today):
    return find_market_open_day(today, True)

def find_market_open_day(today, is_forward):
    if is_forward:
        inc = 1
        num_days = 10
    else:
        inc = -1
        num_days = -10
    current_day = today
    for x in range(0, num_days, inc):
        if is_forward:
            print('-==== {0}'.format(current_day)) 
        if is_market_open(current_day):
            return current_day
        else:
            current_day = add_days_to_date(today, x)

    print('[stock_common] Market closed for a little too long {0}'.format(today))
    sys.exit(0)

def is_market_open(today):
    return os.path.isfile('/Users/osarood/work/cool_predictions/cool_predictions/price_by_date/'+today+'.json')

def get_year(date_str):
    return date_str.split('-')[0]

def get_epoch_time(date_str, slash_format=True, is_hourly=False):
    if not slash_format:
        if is_hourly:
            pattern = '%Y-%m-%d %H'
        else:
            pattern = '%Y-%m-%d'
    else:
        if is_hourly:
            pattern = '%m/%d/%Y %H'
        else:
            pattern = '%m/%d/%Y'
    #pattern = '%m/%d/%Y'
    return int(time.mktime(time.strptime(date_str, pattern)))

def get_random_stocks(stock_list, NUM_STOCKS):
    if NUM_STOCKS > len(stock_list):
        print('We don\'t have enough history!')
        sys.exit(0)
#    return [s['symbol'] for s in stock_list[NUM_STOCKS:]]
    random_stocks = []
    while True:
        random_stock = random.choice(stock_list)
        if random_stock['symbol'] not in random_stocks:
            random_stocks.append({'symbol': random_stock['symbol']})

        if len(random_stocks) == NUM_STOCKS:
            return random_stocks

def calculate_price_gains(price_recs):
    base_price, start_date = starting_price(price_recs)
    for price_rec in price_recs.values():
        price_rec['price_gain'] = (float(price_rec['price']) - base_price)/base_price * 100.0
        price_rec['base_price']  = base_price

    return price_recs, base_price, start_date

def starting_price(price_recs):
    prices_recs_sorted_date = sort_list([x for x in price_recs.values()], 'date', False)
    return prices_recs_sorted_date[0]['price'], prices_recs_sorted_date[0]['date']

def ending_price(price_recs):
    Y = [x for x in price_recs.values()]
    return sort_list(Y, 'date', False)[len(price_recs)-1]['price']

def current_market_cap(price_recs):
    Y = [x for x in price_recs.values()]
    #print('==dsada= {0}'.format(sort_list(Y, 'date', False)[-1]))
    return sort_list(Y, 'date', False)[-1]['market_cap']

def get_date_iterator(start, end):
    start_date_list = start.split('-')
    end_date_list = end.split('-')
    return dategenerator(date(int(start_date_list[0]), int(start_date_list[1]), int(start_date_list[2])),
        date(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2])))

def get_historical_data(symbol, start, end, historical_data_mgr):

    all_historical = historical_data_mgr.get_stock_historical_data(symbol)
    #print('{0}'.format(all_historical))
    date_range = {}
    start_date_list = start.split('-')
    end_date_list = end.split('-')

    for dt in get_date_iterator(start, end):
        date_str = dt.strftime("%Y-%m-%d")
        day_data = all_historical.get(date_str, 'missing_data')
        #print('DT: {0} {1}'.format(dt.strftime("%Y-%m-%d"), day_data))
        if day_data != 'missing_data':
            date_range[date_str] = day_data

    if len(date_range) == 0:
        return None, None

    #print('====> {0} {1}'.format(symbol, date_range))
    return all_historical, date_range

#TODO: This method should go to HistoricalDataManager
def get_stats_for_period(filtered_stock_list, start, end, historical_data_mgr):
    days_active = {}
    active_stock_list = []
    for idx, stock_info in enumerate(filtered_stock_list):
        stock = {'symbol': stock_info['symbol']}
        all_historical, price_recs = get_historical_data(stock_info['symbol'], start, end, historical_data_mgr)
        # no recs found or 1 price record found
        if price_recs == None or len(price_recs) <= 1:
            days_active[stock['symbol']] = 0
        else:
            days_active[stock['symbol']] = len(price_recs)
            price_list = [price_rec['price'] for price_rec in price_recs.values()]
            start_price, start_date = starting_price(price_recs)
            end_price = ending_price(price_recs)
            if stock['symbol'] not in ['^IXIC']:
                try:
                    stock['market_cap'] = current_market_cap(price_recs)
                except KeyError:
                    stock['market_cap'] = 0.0
            #print('[{4}] ===== {0} {1} {2} {3}'.format(stock_symbol, start_price, end_price, start_date, idx))
            stock['gain'] = (end_price - start_price) / start_price * 100.0
            stock['price_list'] = price_recs
            stock['name'] = stock_info['name']
            stock['all_history'] = all_historical
            stock['price_list'], stock['cost_price'], \
                stock['start_date'] = calculate_price_gains(stock['price_list'])
            active_stock_list.append(stock)

    if not active_stock_list:
        print('ERROR: ******** No stock active ****** ({0}, {1})'.format(start, end))
        sys.exit(0)
    else:
        print('[stock_common] Got {0} stocks. Number of active stocks {1}'.format(
            len(filtered_stock_list),
            len(active_stock_list)
        ))
    return remove_stocks_with_missing_prices_data(days_active, active_stock_list)

def remove_stocks_with_missing_prices_data(days_active, active_stock_list):
    # filter 'new' stocks which have less price records
    MAX_DAYS_ACTIVE = median([x for x in days_active.values()])
    final_stock_list = []
    for idx, stock in enumerate(active_stock_list):
        if days_active[stock['symbol']] >= MAX_DAYS_ACTIVE:
            final_stock_list.append(stock)
        else:
            if False: #disable this print
                print("Removing NEW stock {0} recs: {1} {2}".format(stock['symbol'],
                    days_active[stock['symbol']],
                    MAX_DAYS_ACTIVE
                ))
    print('Num stock after checking for missing data ---> {0}'.format(len(final_stock_list)))
    if not final_stock_list:
        print('ALERT!!! Returning empty history for {0} period:({1}, {2})'.format(filtered_stock_list, start, end))
    return final_stock_list

def add_days_to_date(BASE_DATE_STR, days_to_add):
    b_date = BASE_DATE_STR.split('-')
    BASE_END = str(date(int(b_date[0]), int(b_date[1]), int(b_date[2])) + \
        relativedelta(days=days_to_add)
    )
    return str(BASE_END)

def add_months_to_date(BASE_DATE_STR, months_to_add):
    b_date = BASE_DATE_STR.split('-')
    BASE_END = str(date(int(b_date[0]), int(b_date[1]), int(b_date[2])) + \
        relativedelta(months=months_to_add)
    )
    return str(BASE_END)

def dategenerator(start, end):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

def adjust_stock_split(price_recs, split_date, split_factor):
    for date, price_rec in price_recs.iteritems():
        if price_rec['date'] < split_date:
            price_rec['price'] = price_rec['price'] / split_factor

    return price_recs
        

def detect_split(price_recs):
    Y = [x for x in price_recs.values()]
    prices_sorted_by_date = [x for x in sort_list(Y, 'date', False)]
    idx = 1
    while True:
        split_mult = prices_sorted_by_date[idx-1]['price'] / prices_sorted_by_date[idx]['price']
        # use 1.9 since stock can jump a bit after split. For example GOOGL
        if split_mult >= 1.9:
            # divide all prices older than price_rec[idx]['date'] by split_mult
            return True, prices_sorted_by_date[idx]['date'], split_mult
        if idx == len(prices_sorted_by_date)-1:
            return False, None, None
        else:
            idx += 1

def median(mylist):
    sorts = sorted(mylist)
    length = len(sorts)
    if length == 0:
        return None
    if length == 1:
        return sorts[0]
    if not length % 2:
        return (sorts[length / 2] + sorts[length / 2 - 1]) / 2.0
    return sorts[length / 2]

def basic_stock_info_sorted(file_name, sort_field, current_symbols):
    stock_list = read_stock_list(file_name)
    stock_list = [stock for stock in stock_list if stock['symbol'] not in current_symbols]
    print('Read {0} companies info'.format(len(stock_list)))
    filtered_stock_list = stock_list
    return sort_list(filtered_stock_list, 'market_cap', True)

def sort_list(stock_list, key_to_sort, s_order=False):
    return sorted(stock_list, key=itemgetter(key_to_sort), reverse=s_order)
