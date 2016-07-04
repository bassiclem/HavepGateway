#!/usr/bin/python
import sys, socket, simplejson , urllib2
from StringIO import StringIO
from thread import *

def is_json(myjson):
    try:
        json_object = simplejson.load(myjson)
    except ValueError as e:
        return False
    return True

        
def Main():
        host = ''
        port = 5000
        #url = "http://jsonplaceholder.typicode.com/posts/1"
        
        # req = urllib2.Request(url)
        # opener = urllib2.build_opener()
        # f = opener.open(req)
        # test = f
        
        # try:
                # json_res = simplejson.load(f)
                
        # except ValueError, e: 
                # print "not JSON format"
                # sys.exit()
                
                
                
        # print json_res
                
                
        # for item in json_res:
                # print item
        print ('Welcome to ISensit Gateway!')

        # create an INET, STREAMing socket , address and port is given in tuple
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ('Socket created')
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # bind the socket to port
        try:
                s.bind((host, port))
        except socket.error as msg:
                print ('Bind Failed, Error Code: ' + str(msg[0]) + ' Message ' + msg[1])
                sys.exit()
                
        print ("Listening at " + str(host) + " , " + str(port))
        #listen to one connection at a time
        s.listen(10)
        
        #Function for handling connections. This will be used to create threads
        def clientthread(conn):
                #Sending message to connected client
                conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
                 
                #infinite loop so that function do not terminate and thread do not end.
                while True:
                         
                        #Receiving from client
                        data = conn.recv(1024)
                        reply = 'OK...' + data
                        if not data: 
                                break
                 
                        conn.sendall(reply)
                 
                #came out of loop
                conn.close()
        
        # connection and addr
        c, addr = s.accept()
        print ("Connection from : " + str(addr))
        while True:
                data = c.recv(1024)
                if not data:
                        break

                #json code here
                try:
                        json_object = simplejson.loads(data)
                        
                except ValueError as e:
                        print ("not JSON format")
                        sys.exit()
        #       print simplejson.dumps(json_object, sort_keys=True, indent=4)
                try:
                        print (json_object['client']['ip'])
                        #print json_object
                except KeyError as e:
                        print ("Key not found")
                        sys.exit()
                        
                for item in json_object['client']:
                        print (json_object['client'][item])
                
                data = str(data).upper()
                print ("sending : " + str(data))
                c.send(data)
        c.close()
        
if __name__ == '__main__':
        Main()
