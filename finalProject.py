#import winsound, time, csv, audiere, wave #For sound
import csv
from mpl_toolkits.basemap import Basemap
from FileReader import *
from math import *
import numpy as np
import matplotlib.pyplot as plt
from random import *
from time import clock
from datetime import *
import os.path

fileName = 'Data\\noteFrequency.csv'
csvReader = csv.reader(open(fileName, 'rb'), delimiter=',', dialect = 'excel')

def createNotes():
    notes = {}

    for row in csvReader:
        noteHeader = row[0] #The header for each note
        rowData = []
        if (str(noteHeader) != 'Octave' and str(noteHeader) != 'Note'):
            for data in range(1,len(row)):
                row[data] = float(row[data].split(' ')[0]) #Remove trailing junk
                rowData.append(row[data])
            notes[str(noteHeader)] = rowData #Creates a list of frequencies for each note

    return notes



def wavplay(frequency, pan=0):
    root = Note('C', 3)
    scale = Scale(root, [2, 1, 2, 2, 1, 2, 1])

    chunks = []
    chunks.append(chord(frequency, scale))
    chunk = numpy.concatenate(chunks)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1, input=1)
    stream.write(chunk.astype(numpy.float32).tostring())
    stream.close()
    p.terminate()
##'''Plays a sound buffer with blocking, matlab-style'''
##    device = audiere.open_device()
##    output = device.create_tone(float(frequency))
##    output.pan = pan
##    output.play()

#def wavRecord(

def drawMap(fileName):
    normalMode = False
    #Read in the data:
    dataFileName = 'Data\\' + fileName + '.csv'
    dataReader = ReadInCSV(dataFileName)
    dataSet = dataReader.data

    #Set up the variables:
    counter = 0

    #Subplot coordinates:
    subplotMag = []
    subLats = []
    subLons = []
    
    #dimensions of plot:
    width = 19.20 #1080x1920 (1080p)
    height = 10.80
    
    #Title and Annotation Parameters:
    allSet = False
    if allSet:
        title = 'Earthquakes 1973-2009 (n=17143)'
    else:
        title = 'Worst Earthquakes Recorded 1902-2011 (n=87)'
    fontSize = '25'
    fontFamily = 'serif'
    
    start = clock() #timer function
    
    #for each datarow in the dataset:
    for dataRow in dataSet:
        plt.clf() #Clear the current plot
        counter = int(counter)
        counter += 1 #Increment our counter
        counter = '%06d' % counter #Format the counter with preceding zeros
        imageFileName = 'Images\\' + fileName + str(counter) + '.png' #create file name
        #print os.path.isfile(imageFileName)
        counter = int(counter)

        #Reset variables:
        lats = []
        lons = []
        magnitudes = []
        years = []
        months = []
        days = []
        times = []

        #If there is a magnitude available (something to plot):
        if dataRow['Magnitude'] != '':
            timeElapsed = clock() - start
            if counter % 25 == 0: #every 25 iterations:
                print 'Time elapsed so far: ' + str(timeElapsed) + ' Iteration: ' + str(counter)

            #Subplot Coordinates:
            subplotMag.append(float(dataRow['Magnitude']))
            subLats.append(float(dataRow['Latitude']))
            subLons.append(float(dataRow['Longitude']))

            if not os.path.isfile(imageFileName):
                #print 'writing ' + str(counter)
                #Pull out the lats, lons, magnitudes, and the years:
                lats.append(float(dataRow['Latitude']))
                lons.append(float(dataRow['Longitude']))
                magnitudes.append(float(dataRow['Magnitude']))
                if allSet:
                    years.append(float(dataRow['Year']))
                    months.append(float(dataRow['Month']))
                    days.append(float(dataRow['Day']))
                    times.append(float(dataRow['Time(hhmmss.mm)UTC']))
                else:
                    times.append(dataRow['Date - UTC - Time'])
                    #Format the timestamp:
                    date = times[0].split(' ')[0] #Pulls out just the date
                    date = date.split('/') #Pulls out the / characters
                    
                    date[0] = '%02d' % int(date[0]) #Month
                    date[1] = '%02d' % int(date[1]) #Day
                    date[2] = '%02d' % int(date[2]) #Year
                    date = str(date[0]) + str(date[1]) + str(date[2])
                    
                    months.append(date[0:2])
                    days.append(date[2:4])
                    years.append(date[4:8])                                                                         


                #Subplot variables:
                magnitude = np.array(subplotMag)

                #Scatter plot:            
                plt.subplot(212, axisbg='grey')
                plt.subplot2grid((5,5),(3,0), rowspan=2, colspan=5)
                plt.scatter(subLons, subLats, s=50*magnitude, c=magnitude, cmap=plt.cm.jet, alpha=.5)
                plt.ylabel('Latitude',fontsize=int(fontSize)/1.5, family=fontFamily)
                plt.xlabel('Longitude',fontsize=int(fontSize)/1.5, family=fontFamily)
                plt.yticks(range(-180, 180, 72))
                plt.xticks(range(-180, 180, 36))
                plt.grid(c='grey')

                #For the subplot colorbar:
                cbar = plt.colorbar(orientation='horizontal')
                cbar.set_label('Magnitude', fontsize=int(fontSize)+5, family=fontFamily)
                #The limits of the colorbar:
                plt.clim(1,9)


                #Main subplot:
                plt.subplot(211)
                plt.subplot2grid((5,5),(0,0), rowspan=3, colspan = 5)
                plt.title(title + '\n', fontsize=str(int(fontSize)+10), family=fontFamily)#Set the title            
                #Draw the map:
                m = Basemap(projection='robin', lon_0=-160, resolution='c', area_thresh = 1000)
                m.drawcoastlines(linewidth=2, color='white')
                m.drawmapboundary(fill_color='grey')


                #Convert to numpy arrays:
                x,y = m(lons,lats)
                x = np.array(x)
                y = np.array(y)            
                magnitudes = np.array(magnitudes)

                if allSet:
                    #Create datetime object:
                    years = np.array(years)
                    months = np.array(months)
                    days = np.array(days)
                    times = np.array(times)
                    hhmmss = times[0]
                    hhmmss = '%06d' % hhmmss #Format the hhmmss to always have 6 digits
                    hour = int(hhmmss[0:2])
                    minute = int(hhmmss[2:4])
                    second = int(hhmmss[4:6])            
                    date = datetime(int(years[0]), int(months[0]), int(days[0]), hour, minute, second)
                if not allSet:
                    hhmmss = times[0]
                    hhmmss = hhmmss.split(' ')[1]
                    hour = hhmmss.split(':')[0]
                    hour = int(hour)
                    minute = hhmmss.split(':')[1]
                    minute = int(minute)
                    second = 00
                    date = datetime(int(years[0]), int(months[0]), int(days[0]), hour, minute, second)
                    
                
                #plot the region coordinates:
                m.scatter(x,y, s = 500*magnitudes, c=magnitudes,cmap=plt.cm.jet, marker='o', alpha=1)

                #For the colorbar:
                cbar = plt.colorbar(orientation='vertical')
                cbar.set_label('Magnitude', fontsize=fontSize)
                #The limits of the colorbar:
                plt.clim(1,9)

                #Annotations:
                xy = x,y #Coordinates for the data portion of the annotation
                s = str(float(magnitudes[0]))
                
                textCoords = 1650, 900 #coordinates for the text portion of the annotation
                
                #Plot the annotation:
                plt.annotate(s, xy, xytext=textCoords, xycoords='data', textcoords='figure pixels', arrowprops=None, fontsize=int(fontSize)*3, color='black', family=fontFamily)

                #Annotation for the DateTime:
                s = '{:%Y-%m-%d}\n'.format(date)
                s += '{:%H:%M:%S}\n'.format(date)
                s += '{latitude}, {longitude}'.format(latitude=str(lats[0])+'N', longitude=str(lons[0])+'W') + '\n' #Text string for the annotation
                textCoords = 5, 950
                plt.annotate(s, xy, xytext=textCoords, xycoords='data', textcoords='figure pixels', arrowprops=None, fontsize=fontSize, color='grey', family=fontFamily)

                #For the title:
                counter = '%06d' % counter #convert to formatted string with 6 decimals
                s = 'Iteration: '
                s += str(counter) + '\n'
                s += 'Magnitude: '
                textCoords = 1600, 1000
                plt.annotate(s, xy, xytext=textCoords, xycoords='data', textcoords='figure pixels', arrowprops=None, fontsize=int(fontSize), color='grey', family=fontFamily)



                #Filename stuff:
                #imageFileName = 'Images\\' + fileName + str(counter) + '.png' #create file name
                
                #Set the figure size:
                figure = plt.gcf()
                figure.set_size_inches(width, height)    #Normal HD
                #figure.set_size_inches(76.80, 48.00) #Huge HD
                #figure.set_size_inches(51.20, 32.00) #Large HD

                plt.savefig(imageFileName, dpi=100) #save the plot as a png
    

fileName = 'worst_earthquakes'
#fileName = 'all_earthquakes'

start = clock()#timer function
drawMap(fileName)
timeElapsed = clock() - start
print timeElapsed
