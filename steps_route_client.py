# See extended comments at end of file

import requests
from time import time

def try_route(url, r, m):
    msg = url + '/' + r
    if len(m):
        msg = msg + '?'
        for i in len(m):
            try:
                key=str(m[i][0])
                value=str(m[i][1])
            except:
                print('key-value parse fail at index ' + str(i))
                return 'fail', 0.0
            msg = msg + key + '=' + value
            if i < len(m) - 1: msg = msg + '&'
    toc  = time()
    rmsg = requests.get(msg).text
    tic  = time()
    elapsed_time_ms = (tic - toc)/1000
    return rmsg, elapsed_time_ms

my_ip    = input('What ip address? <Enter')
if not(len(my_ip)): my_ip = '52.34.243.66'
my_url = 'http://' + my_ip + ':8080'
my_route = input("What starting route? (Hit <Enter> to choose 'steps'): ")
if len(my_route) == 0: my_route = 'steps'
my_key = input('What key? (Hit <Enter> to skip): ')
if len(my_key):
    my_value = input('What value?')


if len(my_key): msg = msg + '?' + my_key + '='
print(my_url)
print(my_route)
print(try_route(my_url, my_route, []))



# This Python program is a Client of a particular web service. This means that the
#   Python program exchanges messages with the service (running on a Server in the
#   cloud) in the manner of a conversation. The Client speaks first and the Server
#   replies. 
#
# There are six parts to the message:
#   - an ip address like 'http://123.123.123.12:8080/'
#   - a route like 'vegetablepuzzle' to select a specific part of the service
#   - '?'
#   - a key: Optional detail you want to give the service
#   - '='
#   - a value: Associated with the key. Example 'guess=42'
#

#     try :    vfloat = float(msg) 
#     except : return('etc')
# if not msg_string == 'wigs':  return("This time I need the fourth word of the song 'Satin Doll'...")


