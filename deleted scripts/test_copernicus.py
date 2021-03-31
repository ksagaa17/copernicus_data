from selenium import webdriver
from selenium.webdriver.common.by import By # used for waiting for the page to load
from selenium.webdriver.support.ui import WebDriverWait # used for waiting for the page to load
from selenium.webdriver.support import expected_conditions as EC # used for waiting for the page to load
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as exception
import json
import time


options = webdriver.ChromeOptions()
#options.add_argument("headless")
options.headless = False
#options.add_argument("--window-size=1920,1200")
desired_capabilities = options.to_capabilities()
driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

urls_final = []


# Opening locations webpage
driver.get("https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset")
driver.implicitly_wait(5)
urls = []

lastHeight = driver.execute_script("return document.body.scrollHeight")
while True:
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    time.sleep(3)
    newHeight = driver.execute_script("return document.body.scrollHeight")
    if newHeight == lastHeight:
        break
    
    lastHeight = newHeight
   
driver.quit()

    

    
    
    
    
