"""
This script contains spiders for collecting the urls for the datasets. When a spider is used, an .json file 
is returned with the urls for the datasets at the given webpage.

"""

import scrapy
from logzero import logfile, logger
from selenium import webdriver
from selenium.webdriver.common.by import By # used for waiting for the page to load
from selenium.webdriver.support.ui import WebDriverWait # used for waiting for the page to load
from selenium.webdriver.support import expected_conditions as EC # used for waiting for the page to load
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import selenium.common.exceptions as exception
import json
import time


class CDSUrlsSpiderSpider(scrapy.Spider):
    """
    Collects dataset urls from https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset.
    
    Run this spider with: /main/copernicus_scrape$ scrapy crawl CDS_dataset_urls_spider -o CDS_dataset_urls.json
    """
    # Initializing log file
    logfile("dataset_url_spider.log", maxBytes=1e6, backupCount=3)
    name = "CDS_dataset_urls_spider"
    allowed_domains = ["toscrape.com"]

    # Using a dummy website to start scrapy request
    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_urls)

    def parse_urls(self, response):
        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

        # Opening locations webpage
        start_url = "https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset"
        driver.get(start_url)
        driver.implicitly_wait(5)
        dataset_count = 0

        # Scroll down to load all the dataset urls
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while True:
            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            time.sleep(3)
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
        
        # Identifying datasets
        datasets = driver.find_elements_by_xpath('//a[@class="ng-binding"]')
        # Extracting URLs of locations from a subpage
        for dataset in datasets:
            link = dataset.get_attribute("href")
            dataset_count += 1
            yield {
                   "url": link,
                  }


        logger.info(f"Total number of dataset URLs: {dataset_count} on {start_url}")
        driver.quit()

        
class ADSUrlsSpiderSpider(scrapy.Spider):
    """
    Collects dataset urls from https://ads.atmosphere.copernicus.eu/cdsapp#!/search?type=dataset
    Run this spider with: /main/copernicus_scrape$ scrapy crawl ADS_dataset_urls_spider -o ADS_dataset_urls.json
    """
    # Initializing log file
    logfile("dataset_url_spider.log", maxBytes=1e6, backupCount=3)
    name = "ADS_dataset_urls_spider"
    allowed_domains = ["toscrape.com"]

    # Using a dummy website to start scrapy request
    def start_requests(self):
        url = "http://quotes.toscrape.com"
        yield scrapy.Request(url=url, callback=self.parse_urls)

    def parse_urls(self, response):
        # Use headless option to not open a new browser window
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        desired_capabilities = options.to_capabilities()
        driver = webdriver.Chrome(desired_capabilities=desired_capabilities)

        # Opening locations webpage
        start_url = "https://ads.atmosphere.copernicus.eu/cdsapp#!/search?type=dataset"
        driver.get(start_url)
        driver.implicitly_wait(5)
        dataset_count = 0

        # Scroll down to load all the dataset urls
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while True:
            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            time.sleep(3)
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
        
        # Identifying datasets
        datasets = driver.find_elements_by_xpath('//a[@class="ng-binding"]')
        # Extracting URLs of locations from a subpage
        for dataset in datasets:
            link = dataset.get_attribute("href")
            dataset_count += 1
            yield {
                   "url": link,
                  }


        logger.info(f"Total number of dataset URLs: {dataset_count} on {start_url}")
        driver.quit()
