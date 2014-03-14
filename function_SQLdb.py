__author__ = 'Sabine'

import csv
from datetime import datetime
from datetime import timedelta
import MySQLdb

# function which given a bay (Location Key and a date and time returns the number of spaces occupied)

# filename = "ParkingCashlessTransactionsThisFinYear_head_minimal.csv"

def create_matrices_from_csv(filename):
    Key_dictionary = {}

    db = MySQLdb.connect(host = "parkingdata.chwiixytzmrn.eu-west-1.rds.amazonaws.com",
                         user = "parkingadmin",
                         passwd = "parking",
                         db = "parkingdb")

    with open(filename, 'rb') as dataIn:
        reader = csv.reader(dataIn)
        reader.next()
        for row in reader:
            BayID = row[3]
            date = datetime.strptime(row[0], '%Y-%m-%d')
            datetimeS = row[0] + " " + row[1]
            ST = datetime.strptime(datetimeS, '%Y-%m-%d %H:%M')
            datetimeE = row[0] + " " + row[2]
            ET = datetime.strptime(datetimeE, '%Y-%m-%d %H:%M')

            windowS = datetime.strptime(datetimeS[0:-3], '%Y-%m-%d %H')
            windowE = datetime.strptime(datetimeE[0:-3], '%Y-%m-%d %H')
            windowE += timedelta(hours = 1)
            windowDur = windowE-windowS
            windowDur = windowDur.seconds / 3600

            if BayID not in Key_dictionary:
                Key_dictionary[BayID] = {}

            for park_hour in range(0,windowDur):
                useWindowS = windowS + timedelta(hours = park_hour)
                useWindowE = useWindowS + timedelta(hours = 1)
                if useWindowS not in Key_dictionary[BayID]:
                    Key_dictionary[BayID][useWindowS] = 0

                if not (ET <= useWindowS or ST >= useWindowE):
                    Key_dictionary[BayID][useWindowS] += ((min([ET,useWindowE]) - max([ST,useWindowS])).seconds + 0.0)/3600.0

    # with open('output.csv', 'wb') as t:
    #      writert = csv.writer(t)
    #      for bay in Key_dictionary:
    #          for timeKey in Key_dictionary[bay]:
    #              writert.writerow([bay, timeKey, Key_dictionary[bay][timeKey]])

    cur = db.cursor()
    cur.execute("DELETE FROM BAYEVENT")
    rowID = 0
    for bay in Key_dictionary:
        for timeKey in Key_dictionary[bay]:
            rowID += 1

            # Each row has id, occupiedSpaces, datetime, bayID
            query = "INSERT INTO BAYEVENT VALUES (%s, %s, '%s', %s)" % (rowID, Key_dictionary[bay][timeKey], timeKey, bay)
            try:
                cur.execute(query)
                db.commit()
            except:
                print bay
                db.rollback()
    db.close()

create_matrices_from_csv("ParkingCashlessTransactionsThisFinYear_minimal.csv")
