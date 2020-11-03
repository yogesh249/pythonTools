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
expiryDate='05-Nov-2020'
urlnse='https://www.nseindia.com'
url='https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY&expiryDate=05-Nov-2020'
dateformat='%Y.%m.%d %H:%M:%S' 

def fetch_oi(cepe):
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
        totalOi=calculateTotalOi(s, cepe)
        current_time=getCurrentTime()
        
        with open(expiryDate+'-'+cepe+'.json', "a+") as files:
            files.write(current_time)
            files.write(',')
            files.write(str(totalOi))
            files.write('\n')
        files.close()
        time.sleep(60)
    print('Exiting the loop')
        
def filterPutsUpto500Points(final_dictionary, cepe):
    oiArrayData=[]
    OiMap={}
   
    i=0
    for obj in final_dictionary['filtered']['data']:
        if(cepe=='pe'):
            #if underlyingValue lies between strikePrice-500 and strikePrice
            if(int(obj['PE']['strikePrice'])<=int(obj['PE']['underlyingValue'])<=int(obj['PE']['strikePrice']+500)):
                
                oiArrayData.append(obj['PE'])
        elif (cepe=='ce'):
            #if underlyingValue lies between strikePrice and strikePrice+500
            if(int(obj['CE']['underlyingValue'])<=int(obj['CE']['strikePrice'])
                and int(obj['CE']['strikePrice']-500) <=int(obj['CE']['underlyingValue'])):
                    print('Adding to arrayData')
                    print('strikePrice=',obj['CE']['strikePrice'])
                    print('underlyingValue=',obj['CE']['underlyingValue'])
                    oiArrayData.append(obj['CE'])
    print('Now priting the map')
    OiMap['data']=oiArrayData
    return OiMap

def calculateTotalOi(s, cepe):
    oi=0
    #Now get the JSON from the URL.
    response=s.get(url)
    

    # .decode('utf-8') is used to get rid of b' in the beginning of the repnse that we get 
    # which indicates that it is a byte array.
    StringJson=response.content.decode('utf-8')
    final_dictionary = json.loads(StringJson) 
    #filter Puts for last 500 points below current nifty
    putOiMap=filterPutsUpto500Points(final_dictionary, cepe)
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
    graph_data = open(expiryDate+'-pe.json','r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(datetime.strptime(x, dateformat))
            ys.append(y)
    ax1.clear()
    
    graph_data2 = open(expiryDate+'-ce.json','r').read()
    lines2 = graph_data2.split('\n')
    xs2 = []
    ys2 = []
    for line2 in lines2:
        if len(line2) > 1:
            x2, y2 = line2.split(',')
            xs2.append(datetime.strptime(x2, dateformat))
            ys2.append(y2)
    ax1.plot(xs, ys, label = 'PE', color="green")
    ax1.plot(xs2, ys2, label = 'CE', color="red")
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
def main():
    print('Starting the main function')
    x = threading.Thread(target=fetch_oi, args=('ce',))
    x.start()
    
    y = threading.Thread(target=fetch_oi, args=('pe',))
    y.start()
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
    print('Starting the main function2')

main()
    
