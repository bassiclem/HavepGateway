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

def get_degree():
    print "---------------------------------------------------------------------------------------"
    for id in idList:
	print "id ", id
        state = 0
        accx_max = -2
        accy_max = -2
        accz_max = -2
        for r in resultDict[id]:
#            print "r ",r
            if(accz_max < float(r["values"]["ACCZ"][0])):
	        accx_max = float(r["values"]["ACCX"][0])
	        accy_max = float(r["values"]["ACCY"][0])
	        accz_max = float(r["values"]["ACCZ"][0])
	        rssi = r["values"]["RSSI"][0]
        degreex = 0
#       degreex = getDegree(accx_max, accy_max, accz_max, cal_pitch, accx_max)
        degreey = getDegree(accy_max, accx_max, accz_max, cal_pitch, accx_max)
        degreez = getDegree(accz_max, accx_max, accy_max, cal_pitch, accx_max)
#        total_read = db.read_last_acc_beacon_total_data()
#        old_json = db.read_last_acc_beacon_degree(str(id))

# 	print "old json ", old_json
#         if old_json is None:
#             old_degree = 0
#             state = 0
# 	else:
# 	    old_degree = old_json["beacon_accz"]
# 	    state = old_json["state"]
#
# 	print "old degree ", old_degree
# 	print "state ", state
# 	print ("\n\n****************************\n\n")
#
#   	if old_degree is None:
#             old_degree = 0
#
#         if state is None:
#             state = 0
#
# 	if total_read is not None:
# 	    total_lift = total_read['total_lifts']
# 	    bad_lift = total_read['bad_lifts']
# 	    print(bad_lift , total_lift)
# 	    print('++')
#
# 	else:
#             total_lift = 0
#             bad_lift = 0
#             last_degreez = 0
#             print('--')
#
# 	if(degreez < 20):
# 	    state = 0
#    	    print(' |')
#
#         if(degreez >= 20 and old_degree < 20):
# 	    state = 1
# 	    total_lift = total_lift + 1
#    	    print('  *|')
#
# 	if(degreez >= 80 and state == 1):
#    	    print('  **|')
# 	    print("Y U SO BAD!!")
# 	    state = 2
# 	    bad_lift = bad_lift + 1
#
# #	print "last value ", last_degreez
# 	print "id ", id
# 	print "total_lift ", total_lift
# 	print "bad_lift ", bad_lift
 	db.insert_acc_beacon_data(id, degreex, degreey, degreez, rssi)
# 	print "degrees ", old_degree, degreez
    resultDict.clear()
    del idList[:]
    t = threading.Timer(1.0, get_degree)
    t.start()


       
dev_id = 0
rssi = 0
cal_pitch = 20
# # total_lift = 0
# # bad_lift = 0
# old_degree = 0
idList = []
resultDict = {}

try:
    sock = bluez.hci_open_dev(dev_id)
    print("ble thread started")
except:
    print("error accessing bluetooth device...")
    sys.exit(-1)

hci_le_set_scan_parameters(sock)
hci_enable_le_scan(sock)

try:
    # initialize database reader
    db = ISensitGWMysql()
#    sleeptime = db.sleeptime
    db.connect_to_db()
except Exception as e:
    print("Error in initializing db, reason: ", str(e))
    exit(-1)

t = threading.Timer(1.0, get_degree)
t.start()

while True:
    returnedList = parse_events(sock)

    if returnedList is not None:
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
