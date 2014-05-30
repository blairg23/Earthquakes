from mpl_toolkits.basemap import Basemap
from FileReader import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
from random import *

all_events = True #Set this to False to see just the worst earthquakes

def drawMap():
    #Read in the data:
    if all_events:
        fileName = 'Data\\all_earthquakes.csv'
        title = 'All Earthquakes Between 1973 and 2009'        
    else:
        fileName = 'Data\\worst_earthquakes.csv'
        title = 'Worst Earthquakes Ever Recorded'        
    dataReader = ReadInCSV(fileName)
    dataSet = dataReader.data

    #Set up the variables:

    #lat/lon coordinates of all the earthquakes in the world:
    lats = []
    lons = []
    regions = []
    fatalities = []
    magnitudes = []
    
    #Pacific Ocean Area:
    #m = Basemap(projection='robin',llcrnrlat=-42.553, llcrnrlon=163.828,\
    #            urcrnrlat=57.704,urcrnrlon=-112.5, lon_0=-160, lat_ts=20,resolution='c', area_thresh = 1)

    m = Basemap(projection='robin', lon_0=-160, resolution='c', area_thresh = 1000)
    m.drawcoastlines(linewidth=2)
    #m.fillcontinents(color='white', lake_color='grey')
    m.drawmapboundary(fill_color='white')

    plt.title(title, fontsize=100) 
    #m.bluemarble(scale=.5)
    
    #for each datarow in the dataset:
    for dataRow in dataSet:
        lats.append(float(dataRow['Latitude']))
        lons.append(float(dataRow['Longitude']))
        if all_events == False:
            regions.append(str(dataRow['Region']))
        #If there are any recored fatalities to report:
            if dataRow['Fatalities'] != '':
                fatalities.append(float(dataRow['Fatalities']))
        if dataRow['Magnitude'] != '':
            magnitudes.append(float(dataRow['Magnitude']))
        else:
            magnitudes.append(1.0)
        
    #Convert to numpy arrays:
    x,y = m(lons,lats)
    x = np.array(x)
    y = np.array(y)    
    regions = np.array(regions)
    fatalities = np.array(fatalities)
    magnitudes = np.array(magnitudes)


##    from mayavi import mlab
##    s = mlab.mesh(x, y, magnitudes)
##    mlab.show()
    
    #plot the region coordinates:
    m.scatter(x,y, s = 100*magnitudes, c=magnitudes,cmap=plt.cm.autumn, marker='o', alpha=1)
    #For the colorbar:
    cbar = plt.colorbar(orientation='horizontal')
    cbar.set_label('Magnitude')
    #The limits of the colorbar:
    if all_events:
        plt.clim(1,9)
    else:
        plt.clim(8,9)
##    #Places the name of the region on each earthquake:
##    for name, xpt, ypt in zip(regions, x, y):
##        randomNumber = randint(100000, 1000000)
##        arrow = '<'
##        for x in range(0,randomNumber/10000):
##            arrow += '-' 
##        plt.text(xpt, ypt, str(arrow) +str(name))
    #Save the image as a 7680x4800 .png file:
    if all_events:
        fileName = 'all_earthquakes.png'
    else:
        fileName = 'worst_earthquakes.png'
    figure = plt.gcf()
    #figure.set_size_inches(19.2, 10.8)
    figure.set_size_inches(76.80, 48.00)
    #figure.set_size_inches(51.20, 32.00)
    plt.savefig(fileName, dpi=100)
    print 'we got here'
    #plt.show()

drawMap()
