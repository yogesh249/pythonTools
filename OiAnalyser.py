import json
import requests
urlnse='https://www.nseindia.com'
url='https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY&expiryDate=05-Nov-2020'

print('Hello, world!')
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
    
    #Now get the JSON from the URL.
    response=s.get(url)
    # .decode('utf-8') is used to get rid of b' in the beginning of the repnse that we get 
    # which indicates that it is a byte array.
    StringJson=response.content.decode('utf-8')
   
    final_dictionary = json.loads(StringJson) 
    
    print(final_dictionary['filtered']['data'])
    
    with open("oidata.json", "w") as files:
        files.write(json.dumps(final_dictionary['filtered']['data'], indent=4, sort_keys = True))
    
def main():
   
    fetch_oi()

main()
    