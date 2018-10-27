# The source code has taken from https://www.geeksforgeeks.org/whatsapp-using-python/

from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time 
  
# Replace below path with the absolute path 
# to chromedriver in your computer 
# chrome driver version 2.43 has a problem. 
# But version 2.42 works fine.
driver = webdriver.Chrome('D:\\Software\\chromedriver_win32\\chromedriver.exe')
  
driver.get("https://web.telgram.org/") 
wait = WebDriverWait(driver, 600) 
  
# Replace 'Friend's Name' with the name of your friend  
# or the name of a group. This has to be within '" and "'
target = '"test"'
# Replace the below string with your own message 
string = "Message sent using Python!!!"
# locate your friend...
x_arg ="//span[text()='test']"


#not able to click on test group as of now...
group_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg))) 
#group_title=wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "test")))
group_title.click() 
"""
# This is not working with //div[@dir="selectable-text"], it is working with [@dir="ltr"]
inp_xpath = '//div[@dir="ltr"][@data-tab="1"]'
input_box = wait.until(EC.presence_of_element_located(( 
    By.XPATH, inp_xpath))) 
    
print(input_box)
for i in range(100): 
    input_box.send_keys(string + Keys.ENTER) 
    time.sleep(1) 
"""
