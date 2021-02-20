import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger
import json


class ScrapeSpider(scrapy.Spider):
    # Initializing log file
    logfile("ScrapeSpider.log", maxBytes=1e6, backupCount=3)
    name = "ScrapeSpider"
    allowed_domains = ["https://ads.atmosphere.copernicus.eu/cdsapp#!/search?type=dataset"]

    # Using a dummy website to start scrapy request
    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_urls)

    def parse_urls(self, response):
        # Use headless option to not open a new browser window
        options = webdriver.FirefoxOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Firefox(desired_capabilities=desired_capabilities)

        # Getting the Atnosphere Copernicus dataset webpage
        driver.get("https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-reanalysis-eac4-monthly?tab=overview")

        # Implicit wait gives the DOM time to load
        driver.implicitly_wait(10) 
        
        # Title
        title = driver.find.element_by_class_name("page-header")

        # Explicit wait does not proceed until a condition is fulfilled
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "abstract-text")))
        
        # Description
        descriptions = driver.find.element_by_class_name("abstract-text")
        description_count = 0
        
        for description in descriptions:
            yield {
                "discription": descriptions.text,
            }
            description_count += 1
        
    
        # Explicit wait does not proceed until a condition is fulfilled
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "variables-name")))
        
        
        # Parameters
        parameters = driver.find_elements_by_class_name("variables-name")
        parameter_count = 0
        
        for parameter in parameters:
            yield {
                "parameter": parameters.text,
            }
            parameter_count += 1

        driver.quit()
        
        logger.info(f"Total number of Countries in openaq.org: {parameter_count}")
