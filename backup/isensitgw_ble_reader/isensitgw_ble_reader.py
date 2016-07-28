#!/usr/bin/python
import sys

# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_device_adapter import *
from lib.blescan import *
import bluetooth._bluetooth as bluez
from isensit_sql import *
import time
import threading
import datetime

dev_id = 0
rssi = 0
cal_pitch = 20
idList = []
resultDict = {}
sleeptime = 1.0
running = True

def get_degree():
    print("---------------------------------------------------------------------------------------")
    print (datetime.datetime.now())
    for id in idList:
        print ("id ", id)
        state = 0
        accx_max = -2
        accy_max = -2
        accz_max = -2
        for r in resultDict[id]:
            if accz_max < float(r["values"]["ACCZ"][0]):
            if accz_max < float(r["values"]["ACCZ"][0]):
                accx_max = float(r["values"]["ACCX"][0])
                accy_max = float(r["values"]["ACCY"][0])
                accz_max = float(r["values"]["ACCZ"][0])
                rssi = r["values"]["RSSI"][0]
        degreex = 0
        degreey = getDegree(accy_max, accx_max, accz_max, cal_pitch, accx_max)
        degreez = getDegree(accz_max, accx_max, accy_max, cal_pitch, accx_max)
        db.insert_acc_beacon_data(id, degreex, degreey, degreez, rssi)
    resultDict.clear()
    del idList[:]
    global running
    if running:
        t = threading.Timer(sleeptime, get_degree)
        t.start()
	running = False
    else:
        print ("System exit")

sock = hci_start_scan(dev_id)

try:
    # initialize database reader
    db = ISensitGWMysql()
  #  sleeptime = db.sleeptime
   # print(sleeptime)
    db.connect_to_db()
except Exception as e:
    print("Error in initializing db, reason: ", str(e))
    running = False
    exit(-1)

if running:
    t = threading.Timer(sleeptime, get_degree)
    t.start()
else:
    print "System exit"

while True:
    print ("Executing while")
    running = True
    returnedList = parse_events(sock)
#    print ("thread count: ", threading.activeCount())
#    for th in threading.enumerate():
#        print ("thread : ", th) 
    
    if returnedList is not None:
	if returnedList is not False:
            id = returnedList["device_info"]["ID"][0]
            if (id not in idList):
                idList.append(id)
                resultList = []
                resultList.append(returnedList)
                resultDict[id] = resultList
            else:        
                resultList = resultDict[id]
                resultList.append(returnedList)
                resultDict[id] = resultList

# time.sleep(1)
db.close()
