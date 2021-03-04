
point_click = tuple()

def nearest(items, pivot):
    nearest = min(items, key=lambda x: abs(x - pivot))
    timedelta = abs(nearest - pivot)
    return nearest, timedelta

# def onpick(event):
#     thisline = event.artist
#     xdata = thisline.get_xdata()
#     ydata = thisline.get_ydata()
#     ind = event.ind
#     print('onpick points:', *zip(xdata[ind], ydata[ind]))
#     global point_click
#     point_click = (xdata[ind], ydata[ind])

def on_pick(event):
    thisline  = event.artist
    xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
    x, y = thisline .get_xdata(), thisline.get_ydata()
    ind = event.ind
    print('Artist picked:', thisline)
    print('{} vertices picked'.format(len(ind)))
    print('Pick between vertices {} and {}'.format(min(ind), max(ind)+1))
    print('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
    print('Data point:', x[ind[0]], y[ind[0]])
    print()
    global point_click
    point_click = (x[ind[0]], y[ind[0]])