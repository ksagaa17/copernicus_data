import scrapy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as exception
from logzero import logfile, logger
import json



class CopernicusSpider(scrapy.Spider):

    # Initializing log file
    logfile("openaq_spider.log", maxBytes=1e6, backupCount=3)
    name = "urls_spider"
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

        # Implicit wait
        driver.implicitly_wait(10)

        # Explicit wait
        wait = WebDriverWait(driver, 5)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "variables-name")))

        

        # parameters
        parameters = driver.find_elements_by_class_name("variables-name")
        parameter_count = 0
        
        for parameter in parameters:
            yield {
                "parameter": parameters.text,
            }
            parameter_count += 1

        driver.quit()
        
        logger.info(f"Total number of Countries in openaq.org: {parameter_count}")
