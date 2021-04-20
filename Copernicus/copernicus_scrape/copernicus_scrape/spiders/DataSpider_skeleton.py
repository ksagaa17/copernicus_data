"""
This script contains spiders for collecting the title, description and
parameters for a dataset on the Copernicus database 
an .json file is returned with the entities for a given website.
"""


import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger
import json


class ScrapeSpider(scrapy.Spider):
    """
    Scrapes: https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4-monthly?tab=overview
    And returns a .json file with the title, description and parameters of the page
    Run this spider with: /main/copernicus_scrape$ scrapy crawl ScrapeSpider -o ScrapeSpider.json 
    """
    # Initializing log file
    logfile("ScrapeSpider.log", maxBytes=1e6, backupCount=3)
    name = "ScrapeSpider2"
    allowed_domains = ["toscrape.com"]

    # Using a dummy website to start scrapy request
    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_urls)

    def parse_urls(self, response):
        # Use headless option to not open a new browser window
        # options = webdriver.FirefoxOptions()
        # options.add_argument("headless")
        # desired_capabilities = options.to_capabilities()
        # driver = webdriver.Firefox(desired_capabilities=desired_capabilities)
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)
        
        
        with open("ADS_dataset_urls.json", "r") as f:
            temp_list = json.load(f)

        url_list = list(map(lambda x: x["url"], temp_list))
        total_url_count = 0
        for i, url in enumerate(url_list):
            

            # Getting the Atnosphere Copernicus dataset webpage
            driver.get(url)

            # Implicit wait gives the DOM time to load
            driver.implicitly_wait(10) 
            
            ### MORTENS DEL ###
            
            ###################
            
            total_url_count += 1
            logger.info("{} Total number of parameters and {} Total number of descriptions for url no. {}".format(parameter_count, description_count, total_url_count))
        logger.info("{} Total number of urls scraped".format(total_url_count))
        
        driver.quit()
        
    
