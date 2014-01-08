############################################################################################################
#Author: Blair Gemmer
#Last Editted: 10/20/11
#Class: CSCI 444 - Data Visualization
#Semester: Fall 2011
#Program: FileReader.py
#Purpose: Reads in a file, parses the file and outputs the raw data as objects to be analysed.
#
#Notes: *Rewrote ParseFile method for better readability.
#       *Removed Classifiers as an attribute
############################################################################################################

#!/usr/bin/python
#imports csv file reader and system commands:
import csv, sys

############################################################################################################
#Class: ReadInCSV
#Input: fileName of CSV file
#Output: Analysis of CSV file
#Purpose: reading in a given csv and creating an array from that file data, then doing analysis on the file
#and outputting the analysis.
############################################################################################################
class ReadInCSV:
    def __init__(self, fileName):
        #instantiate the CSV file variable:
        self.fileName = fileName
        print '----------------------------------------'
        print '\n\nloading file: ' + self.fileName + '...\n'
        #start parsing the file:
        self.data, self.attributes = self.ParseFile() #self.classifiers,
        #if we want to prompt the user for more information:
        #self.PromptUser()
        print self.fileName + ' loaded successfully!\n\n'
        print '----------------------------------------'
        
    #Read in and parse a CSV file into columns,rows
    #Creates separate arrays for header row, classifier rows, and data items:
    def ParseFile(self):
        try:
            #open the csv file:
            with open(self.fileName, 'rb') as csv_file:
                #set the header row:
                attrHeaderRow = csv_file.readline().strip()

                #parse out the attributes from that header row:
                attributes = [attr.strip() for attr in attrHeaderRow.split(",")]

                #parse out all the lines in the csv file:
                lines = [line.strip() for line in csv_file.readlines()]

                #remove the attributes line from the list of lines:
#               del lines[0]

                #parse out the individual data records from the given file:
                data = []
                for line in lines:
                    data.append(dict(zip(attributes, [datum.strip() for datum in line.split(",")])))
                    
##                #parse out the individual classifiers for each data record:
##                classifiers = []
##                classifiers = [record[attributes[-1]] for record in data]
                    
            #Return those attributes and the data points:
            return data, attributes#, classifiers
        
        #unless we hit an error in the csv file:
        except csv.Error, e:
            #in which case, we exit the program and print the error code:
            sys.exit('file %s, line %d: %s' % (self.fileName, row, e))


    def PromptUser(self):
        #prompt the user for file information:
        userInput = None
        while not userInput:
            try:
                userInput = str(raw_input('press i for more information, or any other key to continue...'))
            except ValueError:
                print 'press i for more information, or any other key to continue...'
            if userInput == 'i':
                print 'dimensions: ' + str(self.attributes)
                #uncomment this for testing the data values returned:
                #print 'data: ' + str(self.data)
                print '----------------------------------------'
            else:
                print '----------------------------------------'

                
       
#Test Driver:
#fileName = 'Data\\trainingDataCandElim.csv'
##fileName = 'social_data.csv'
##readTrainingData = ReadInCSV(fileName)
##readTrainingData.PromptUser()
##
##
##fileName = 'Training Data\\DblInt.csv'
##readTrainingData = ReadInCSV(fileName)
##
##
##fileName = 'Training Data\\DblStr.csv'
##readTrainingData = ReadInCSV(fileName)
##
##fileName = 'Training Data\\IntInt.csv'
##readTrainingData = ReadInCSV(fileName)
##
##
##fileName = 'Training Data\\IntStr.csv'
##readTrainingData = ReadInCSV(fileName)
##
##fileName = 'Training Data\\StrInt.csv'
##readTrainingData = ReadInCSV(fileName)
##
##fileName = 'Training Data\\StrStr.csv'
##readTrainingData = ReadInCSV(fileName)


############################################################################################################
