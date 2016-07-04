import sys

# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_cloud import *
from isensit_sql import *
import threading


jsonDict = {}
deviceInfoDict = {}
deviceValueDict = {}
row_count = 0
sleeptime = 4.0
#try:
    # initialize database reader
#    a = 2
#except Exception as e:
#    print("Error in initializing db, reason: ", str(e))
#    exit(-1)

uploader = ISensitCloud()
data = None
count = 0
db = ISensitGWMysql()

def getData():
    try:
#        db = ISensitGWMysql()
#	if db.isConnected() is not None:
#	    db.close_db()
        db.connect_to_db()
        data = db.read_first_five_beacon_data()
        if data is None:
            print("No data left")
        else:
	    for index in range(len(data)):
#		row_count = data[index]["row_count"]
#        	deviceInfoDict['UUID'] = data[index]["beacon_uuid"]
#                deviceInfoDict['ID'] = data[index]["beacon_major"]
#                deviceValueDict['minor'] = data[index]["beacon_minor"]
#                deviceValueDict['rssi'] = data[index]["beacon_rssi"]

#                jsonDict['gatewayID'] = db.gatewayID
#                jsonDict["device"] = deviceInfoDict
#                jsonDict["values"] = deviceValueDict
#		print row_count
#		print data[index]["row_count"], ": ", jsonDict["device"]["ID"]
#                print "data ", index, ": ", jsonDict
		if data[index] is not None:
		    t = threading.Thread(target = uploadData, args = (data[index],))
		    t.setDaemon(True)
		    t.start()
#            row_count = data["row_count"]
#            deviceInfoDict['ID'] = data["beacon_id"]
#            deviceValueDict['accx'] = data["beacon_accx"]
#            deviceValueDict['accy'] = data["beacon_accy"]
#            deviceValueDict['accz'] = data["beacon_accz"]
#            deviceValueDict['rssi'] = data["beacon_rssi"]
            
#            row_count = data["row_count"]
#            deviceInfoDict['UUID'] = data["beacon_uuid"]
#            deviceInfoDict['ID'] = data["beacon_major"]
#            deviceValueDict['minor'] = data["beacon_minor"]
#            deviceValueDict['rssi'] = data["beacon_rssi"]

#            jsonDict['gatewayID'] = db.gatewayID
#            jsonDict["device"] = deviceInfoDict
#            jsonDict["values"] = deviceValueDict
            # data = json.dumps(deviceInfoDict, ensure_ascii=False)

#            print(jsonDict)

    except Exception as e:
        print("Error in Aws Sender, reason: ", str(e))
    else:
        if data is not None:
            print("uploading...")
#	    uploadData()
#            db.delete_acc_beacon_data(row_count)
#            upload = uploader.post_data(jsonDict)

#            if upload:
#                print("upload successful, deleting row..")
#                db.delete_acc_beacon_data(row_count)

#            else:
#                print("Data was not uploaded reason: ")
#                print(upload)
        db.close_db()
    	t = threading.Timer(sleeptime, getData)
	t.start()


def uploadData(dataj):
    try:
	if(dataj is not None):
	    rowcount = dataj["row_count"]
	    create_at = dataj["created_at"]
            deviceInfoDict['UUID'] = dataj["beacon_uuid"]
            deviceInfoDict['ID'] = dataj["beacon_major"]
            deviceValueDict['minor'] = dataj["beacon_minor"]
            deviceValueDict['rssi'] = dataj["beacon_rssi"]

            jsonDict['gatewayID'] = db.gatewayID
            jsonDict["device"] = deviceInfoDict
            jsonDict["values"] = deviceValueDict

#	    print "row count ", rowcount, "upload Data :", jsonDict["device"]["ID"]

    	upload = uploader.post_data(jsonDict)
	print rowcount, "upload ",upload
    	if upload:
            print("upload successful, deleting row..")
            db.connect_to_db()
            db.delete_acc_beacon_data(rowcount)

        else:
            print("Data was not uploaded reason: ")
            print(upload)
	 
    except Exception as e:
        print(rowcount, "Error in Upload , reason: ", str(e))
        db.close_db()


getData()

