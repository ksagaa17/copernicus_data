"""
This script contains spiders for collecting the title, description and
parameters for a dataset on the Copernicus Atmosphere Data Store database 
an .json file is returned with the entities for a given website.
"""


import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger
import json


class ADSDataSpider(scrapy.Spider):
    """
    Scrapes: https://ads.atmosphere.copernicus.eu/cdsapp#!/search?type=dataset
    And returns a .json file with the title, description and parameters of the page
    Run this spider with: /main/copernicus_scrape$ scrapy crawl ADSDataScrapeSpider -o data/ADS_data.json 
    """
    # Initializing log file
    logfile("DataScrapeSpider.log", maxBytes=1e6, backupCount=3)
    name = "ADSDataScrapeSpider"
    allowed_domains = ["toscrape.com"]

    # Using a dummy website to start scrapy request
    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_urls)

    def parse_urls(self, response):
        #Use headless option to not open a new browser window

        # FIREFOX
        # options = webdriver.FirefoxOptions()
        # options.add_argument("headless")
        # desired_capabilities = options.to_capabilities()
        # driver = webdriver.Firefox(desired_capabilities=desired_capabilities)
        
        # CHROME
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        
        # Get urls
        with open("data/ADS_dataset_urls.json", "r") as f:
            temp_list = json.load(f)

        url_list = list(map(lambda x: x["url"], temp_list))
        total_url_count = 0
        for i, url in enumerate(url_list):
            

            # Getting the Atnosphere Copernicus dataset webpage
            driver.get(url)

            # Implicit wait gives the DOM time to load
            driver.implicitly_wait(10) 
            
            # Explicit wait does not proceed until a condition is fulfilled
            wait = WebDriverWait(driver, 5)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "page-header")))
        
            # Title
            header = driver.find_elements_by_class_name("page-header")
            text = header[0].get_attribute("innerText")
            # for head in header:    
                #     text = head.get_attribute("innerText")
                #     yield {
                #         "title": text
                #         }
                # Explicit wait does not proceed until a condition is fulfilled
            wait = WebDriverWait(driver, 5)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "abstract-text")))
        
            # Description
            descriptions = driver.find_elements_by_class_name("abstract-text")
            description_count = 0
            tmp1 = []
        
            for description in descriptions:
                tmp1.append(description.get_attribute("innerText"))
                description_count += 1
        
    
            # Explicit wait does not proceed until a condition is fulfilled
            # wait = WebDriverWait(driver, 5)
            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "variables-name")))
        
        
            # Parameters
            parameters = driver.find_elements_by_class_name("variables-name")
            parameter_count = 0
            tmp2 = []
        
            for parameter in parameters:
                if parameter.get_attribute("innerText") != "Name":
                    tmp2.append(parameter.get_attribute("innerText"))
                    parameter_count += 1
                
            yield {
                "Webpage": url,
                "Title": text,
                "Description": tmp1,
                "Parameters": tmp2
                }
            
            total_url_count += 1
            logger.info("{} Total number of parameters and {} Total number of descriptions for url no. {}".format(parameter_count, description_count, total_url_count))
        logger.info("{} Total number of urls scraped".format(total_url_count))
        
        driver.quit()
        
    
