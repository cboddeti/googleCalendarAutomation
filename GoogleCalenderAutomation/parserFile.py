import csv
import datetime

csvFile = open('scheduleFile.csv','r')

readerFile = list(csv.reader(csvFile,delimiter=','))
sortedlist = sorted(readerFile[1:], key=lambda row: row[0], reverse=False)

for row in sortedlist:
    startTime = row[1].split(' ')[0] + 'T' + row[1].split(' ')[1].split(':')[0] + ':00:00'
    endTime = row[1].split(' ')[0] + 'T' + row[1].split(' ')[1].split(':')[0] + ':30:00'
    print({startTime,endTime,row[2]})
#need to parse this into json with entries and give it as a body