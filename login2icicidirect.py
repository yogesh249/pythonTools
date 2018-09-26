#This is still not working, need to be worked upon

import requests, bs4
"""javascript:function E()
{
try
{f0=document.getElementById('form1');
f0['ctl00$ContentPlaceHolder1$txtUserId'].value='GODKNOWS';
f0['ctl00$ContentPlaceHolder1$txtPass'].value='reliance4';
f0['ctl00$ContentPlaceHolder1$txtDOB'].value='24091982';
}catch(err)
{alert(err.description);}}
E()
"""
usernameData = {'txtUserId':"GODKNOWS",
                'txtPass':"reliance4",
                'txtDOB':"24091982"
                }

import os
cwd = os.getcwd()
print(cwd)
# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    res = s.post('https://secure.icicidirect.com/IDirectTrading/customer/login.aspx', usernameData)
    with open('testResponse.html', 'w') as testRes:
        testRes.write(res.text)
        
    # An authorised request.
    r = s.get('https://secure.icicidirect.com/IDirectTrading/Trading/Equity/iClick2Gain.aspx')

    with open('iClick2Gain.html', 'w') as f:
        f.write(r.text)
        # etc...
