# Copernicus Data

## Introduction
This is the code and data used for scraping the Copernicus datastors *Atmosphere Data Store* and *Climate Data Store*. These are found here:
- https://ads.atmosphere.copernicus.eu/cdsapp#!/search?type=dataset
- https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset

The project includes 
- Scraping the data stores
- Adding the data to Elasticsearch
- Compute Jaccard distance between datasets

Most of the code is written in python 3.8.6 and the scraping and adding to Elasticsearch has been done in Linux, more specifically on Ubuntu 20.10. Therefore, the documentation is based on the fact that we used Ubuntu, but similar commands may exists for Windows and MacOS.

For this project we have used:
- scrapy 2.4.1  
- selenium 3.141.0  
- elasticsearch 7.11.1
- kibana 7.11.1

Other dependencies:
- logzero 1.6.3 
- numpy 1.19.2
- nltk 3.5
- re 2.2.1
- json 2.0.9

Elasticsearch is based on java and therefore we need Open JDK 11 on our machine. 

### References
We have used the following as inspiration for implementation and installation
- https://towardsdatascience.com/web-scraping-with-selenium-d7b6d8d3265a
- https://www.digitalocean.com/community/tutorials/how-to-install-elasticsearch-logstash-and-kibana-elastic-stack-on-ubuntu-20-04
- https://stackoverflow.com/questions/33980591/insert-multiple-documents-in-elasticsearch
- http://brandonrose.org/clustering

## Installations
We will breifly descripe the installation of the pakages. 

### Open JDK 11
Update pakage index:
```shell
$ sudo apt update
```
Install the default Java Runtime Environment (JRE), which will install the JRE from OpenJDK 11:
```shell
$ sudo apt install default-jre
```

### Elasticsearch
You can either download the most recent pakage from https://www.elastic.co/start or install directly from the terminal.
First the Elasticsearch must be added to the pakages index
```shell
$ curl -fsSL https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
$ echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
```
Update apt
```shell
$ sudo apt update
```
and finally install Elasticsearch
```shell
$ sudo apt install elasticsearch
```
Now, we are ready to start Elasticsearch
```shell
$ sudo systemctl start elasticsearch
$ sudo systemctl enable elasticsearch
```
The second command ensures that Elasticsearch starts at systemboot. Elasticsearch run per default on localhost:9200.

### Kibana
Install Kibana after Elasticsearch.
```shell
$ sudo apt install kibana
$ sudo systemctl enable kibana
$ sudo systemctl start kibana
```
Kibana will per default run on localhost:5601

### Scrapy
Installing scrapy is easy on linux. 
```shell
$ pip install scrapy
```
### Selenium 
Installing selenium is also easy on linux. 
```shell
$ pip install selenium
```
In order to use selenium, we need a webdriver. We have used Chrome and Firefox. Installing the ChromeDriver is done by
```shell
$ wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
$ unzip chromedriver_linux64.zip
$ sudo mv chromedriver /usr/local/bin/
```
Installing the Firefox driver is done by
```shell
$ sudo apt install firefox-geckodriver
```

## Scraping the data stores
First we create a scrapy project named copernicus_scrape
```shell
$ scrapy startproject copernicus_scrape
```
In the script settings.py we enable AutoThrottle and set start delay to 5.
```
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False
```
We then created the spiders in the spiders folder using both Scrapy and Selenium. The webpages are scraped by first running the spiders in the dataset_url_spider.py by 
```shell
/main/copernicus_scrape$ scrapy crawl CDS_dataset_urls_spider -o data/CDS_dataset_urls.json
/main/copernicus_scrape$ scrapy crawl ADS_dataset_urls_spider -o data/ADS_dataset_urls.json
```
The urls are stored in the json files CDS_dataset_urls.json and ADS_dataset_urls.json. Afterwards the datascraping spiders are run by 
```shell
/main/copernicus_scrape$ scrapy crawl CDSScrapeSpider -o data/CDS_data.json 
/main/copernicus_scrape$ scrapy crawl ADSScrapeSpider -o data/ADS_data.json 
```
The data is stored in the files CDS_data.json and ADS_data.json in copernicus_scrape/data.

## Adding data to Elasticsearch
In order to add the data to Elasticsearch we use the bulk API. This is described in https://stackoverflow.com/questions/33980591/insert-multiple-documents-in-elasticsearch.
We use the scrpits CDS_bulk.sh and ADS_bulk.sh to add the data to Elasticsearch and these are found in the Elasticsearch folder. This is done by first editing the script and then running it:
```shell
/Elasticsearch$ nano ADS_bulk.sh
/Elasticsearch$ chmod u+x ADS_bulk.sh
/Elasticsearch$ ./ADS_bulk.sh
```
Opening http://localhost:5601, we can under Manage click on Index Management and see that we have added the data to Elasticsearch.

## Compute Jaccard distance between datasets
We use the data in the data folder. In order to use the tools in the nltk module we must first download the content using
```python
import nltk
nltk.download()
```
This should open a window from which we can download what we need. 
We use the Snowball stemmer and the list of stopwords included in nltk.

All the scripts used for the jaccard distance can be found in the Clustering folder.

[comment]: <> (git remote add origin https://github.com/ksagaa17/copernicus_data.git)

[comment]: <> (pull with git pull origin main)
