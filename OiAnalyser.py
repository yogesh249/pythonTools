import json
import requests
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
import time
import logging
import threading
urlnse='https://www.nseindia.com'
url='https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY&expiryDate=05-Nov-2020'
dateformat='%Y.%m.%d %H:%M:%S' 

def fetch_oi():
    s = requests.Session()
    # These 4 headers are required to connect to nseindia url.
    s.headers.update({'referer': 'https://www.nseindia.com/get-quotes/derivatives?symbol=NIFTY&identifier=OPTIDXNIFTY29-10-2020CE12000.00'})
    s.headers.update({'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'})
    s.headers.update({'accept-language':'en-US,en;q=0.9,hi;q=0.8'})
    s.headers.update({'accept-encoding':'gzip, deflate, br'})
    rs=s.get(urlnse)
    #Now its time to set all the cookies we recieved from nseindia, so that we can get the JSON
    for name,value in rs.cookies.items():
        s.cookies.set(name,value)    
    
    xar = []
    yar = []
    
    while True:
        totalOi=calculateTotalOi(s)
        current_time=getCurrentTime()
        
        with open("oidata.json", "a+") as files:
            files.write(current_time)
            files.write(',')
            files.write(str(totalOi))
            files.write('\n')
        files.close()
        
        #graphRawFX()
        time.sleep(60)
    print('Exiting the loop')
        
def filterPutsUpto500Points(final_dictionary):
    putOiArrayData=[]
    putOiMap={}
   
    i=0
    for obj in final_dictionary['filtered']['data']:
        
        if(int(obj['PE']['underlyingValue']-500)<int(obj['PE']['strikePrice']) and int(obj['PE']['underlyingValue'])>int(obj['PE']['strikePrice'])):
            putOiArrayData.append(obj['PE'])
    print('Now priting the map')
    putOiMap['data']=putOiArrayData
    return putOiMap

def calculateTotalOi(s):
    oi=0
    #Now get the JSON from the URL.
    response=s.get(url)
    

    # .decode('utf-8') is used to get rid of b' in the beginning of the repnse that we get 
    # which indicates that it is a byte array.
    StringJson=response.content.decode('utf-8')
    final_dictionary = json.loads(StringJson) 
    #filter Puts for last 500 points below current nifty
    putOiMap=filterPutsUpto500Points(final_dictionary)
    #print(putOiMap)
    for obj in putOiMap['data']:
          print('oi = ', obj['openInterest'])
          oi=oi+int(obj['openInterest'])
    return oi

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime(dateformat)
    print("Current Time =", current_time)
    return current_time  
def animate(i):
    graph_data = open('oidata.json','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(datetime.strptime(x, dateformat))
            ys.append(y)
    ax1.clear()
    ax1.plot(xs, ys)
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
def main():
    print('Starting the main function')
    x = threading.Thread(target=fetch_oi, args=())
    x.start()
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
    print('Starting the main function2')

main()
    
