from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Fill in the username and password here.
user = ""
pwd = ""
#install the chrome driver into below location, before invoking this script.
driver = webdriver.Chrome('D:\\Software\\chromedriver_win32\\chromedriver.exe')
driver.get("http://www.facebook.com")
assert "Facebook" in driver.title
elem = driver.find_element_by_id("email")
elem.send_keys(user)
elem = driver.find_element_by_id("pass")
elem.send_keys(pwd)
elem.send_keys(Keys.RETURN)
