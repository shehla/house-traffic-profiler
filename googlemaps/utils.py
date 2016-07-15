from operator import itemgetter
import time
import datetime

def convert_to_epoch(day):
    cur_d =  datetime.datetime(int(day.split('-')[2]),int(day.split('-')[1]),int(day.split('-')[0]))
    return int(cur_d.strftime('%s'))

def convert_to_epoch_slash_format(day):
    print(day)
    cur_d =  datetime.datetime(int(day.split('/')[2]),int(day.split('/')[0]),int(day.split('/')[1]))
    return int(cur_d.strftime('%s'))

def convert_to_epoch_slash_format_hour(day_time):
    day = day_time.split()[0]
    cur_d =  datetime.datetime(int(day.split('/')[2]),int(day.split('/')[0]),int(day.split('/')[1]), int(day_time.split()[1]))
    return int(cur_d.strftime('%s'))

def convert_to_epoch_slash_format_min(day_time):
    day = day_time.split()[0]
    cur_d =  datetime.datetime(int(day.split('/')[2]),int(day.split('/')[0]),int(day.split('/')[1]), int(day_time.split()[1].split(':')[0]), int(day_time.split()[1].split(':')[1]))
    return int(cur_d.strftime('%s'))

def sort_list(stock_list, key_to_sort, s_order=False):
    return sorted(stock_list, key=itemgetter(key_to_sort), reverse=s_order)

def sort_list_by_date(recs, key_to_sort, s_order=False):
    for x in recs:
        pattern = '%m/%d/%Y %H'
        x['__epoch'] = int(time.mktime(time.strptime(x['date'], pattern)))
    return sorted(recs, key=itemgetter('__epoch'), reverse=s_order)
