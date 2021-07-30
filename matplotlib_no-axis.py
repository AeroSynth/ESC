import numpy
from matplotlib import pyplot

x = numpy.arange(10)
y = numpy.array([5,3,4,2,7,5,4,6,3,2])

fig = pyplot.figure()#frameon=False)
ax = fig.add_subplot(111) #111 is optional

''' next 3 instructions remove frames and axis '''
ax.set_frame_on(False)
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

pyplot.plot(x,y)

for i,j in zip(x,y):
    ax.annotate(str(j),xy=(i,j))

pyplot.show()
