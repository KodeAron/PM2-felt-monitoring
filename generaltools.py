import numpy as np
import math

point_click = tuple()

def main():
    testlista = [4, 5, 6 ,1 ,-1, 8]
    breaches = count_breaches(testlista, upper_threshold= 4)
    print(breaches)

def nearest(items, pivot):
    nearest = min(items, key=lambda x: abs(x - pivot))
    timedelta = abs(nearest - pivot)
    return nearest, timedelta

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
    
# def onpick(event):
#     thisline = event.artist
#     xdata = thisline.get_xdata()
#     ydata = thisline.get_ydata()
#     ind = event.ind
#     print('onpick points:', *zip(xdata[ind], ydata[ind]))
#     global point_click
#     point_click = (xdata[ind], ydata[ind])

if __name__ == '__main__':
    main()