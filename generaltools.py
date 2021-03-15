import numpy as np
import math
import datetime as dt

point_click = tuple()

def main():
    # testlista = [4, 5, 6 ,1 ,-1, 8]
    # breaches = count_breaches(testlista, upper_threshold= 4)
    # print(breaches)
    datetime_list = [dt.datetime(2020,11,5,6,0), dt.datetime(2020,12,3,15,15),dt.datetime(2020,12,7,0,15)]
    new_dates = extract_date_list(datetime_list,dt.datetime(2020,12,5))#,dt.datetime(2020,12,8))
    print(new_dates)

def nearest(items, pivot):
    nearest = min(items, key=lambda x: abs(x - pivot))
    timedelta = abs(nearest - pivot)
    return nearest, timedelta

def is_date_between(check_date, first_date, last_date):
    pass
    return # isbetween # true if check_date lies between first_date and last_date

def extract_date_list(list_of_dates, first_date=None, last_date=None):
    ''' extract a list of dates from (ordered) list/series 
    by specifying first and last date
    all dates in datetime format
    '''
    extracted_dates=[]
    for item in list_of_dates:
        if (first_date==None or (item>first_date))\
             and (last_date==None or (item<last_date)):
            extracted_dates.append(item)
    return extracted_dates

def count_breaches(list_of_values, lower_threshold=-math.inf, upper_threshold=math.inf):
    nBreaches_lower = sum(x < lower_threshold for x in list_of_values)
    nBreaches_upper = sum(x > upper_threshold for x in list_of_values)
    return nBreaches_lower, nBreaches_upper

def on_pick(event):
    thisline  = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    x, y = thisline .get_xdata(), thisline.get_ydata()
    ind = event.ind
    print('Artist picked:', thisline)
    print('{} vertices picked'.format(len(ind)))
    print('Pick between vertices {} and {}'.format(min(ind), max(ind)+1))
    print('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
    xval = x[ind[0]]
    yval = y[ind[0]]
    if type(xval)==np.datetime64:
        print('np.datetime64')
        xval = datetime64_to_datetime(xval)
    print('Data point:', xval, yval)
    global point_click
    point_click = (xval, yval)

def datetime64_to_datetime(np_datetime64):
    print('(np.datetime64 -> datetime) ',end='')
    datetime = np_datetime64.astype('M8[ms]').astype('O')
    print(np_datetime64,end='')
    print(' -> ',end='')
    print(datetime)
    return datetime
    
def all_values_from_key(listofdicts, keyword):
    value_list = []
    for item in listofdicts:
        value_list.append(item[keyword])
    return value_list

def compare_dicts(dict1, dict2, find_similarities=False):
    """Compare two dictionaries.
    Input two dictionaries to compare. 
    find_similarities: look for similiarities if True, look for differences if False.
    """
    k1 = set(dict1.keys())
    k2 = set(dict2.keys())
    common_keys = set(k1).intersection(set(k2)) # find all keys that appear in both dictionaries
    if find_similarities:
        print('Looking for SIMILARITIES between dictionaries')
        for key in common_keys:
            if key not in ['x','data'] and dict1[key] == dict2[key] :
                print (key + ": " + str(dict1[key]) + " matches " + str(dict2[key]))
    else:
        print('Looking for DIFFERENCES between dictionaries')
        for key in common_keys:
            if key not in ['x','data'] and dict1[key] != dict2[key] :
                print (key + ": " + str(dict1[key]) + " differs from " + str(dict2[key]))


if __name__ == '__main__':
    main()