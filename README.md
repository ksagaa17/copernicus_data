# Copernicus Data

## Introduction
This is the code and data used for scraping the Copernicus datastores *Atmosphere Data Store* and *Climate Data Store*. These are found here:
- https://ads.atmosphere.copernicus.eu/cdsapp#!/search?type=dataset
- https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset

The project includes 
- Scraping the data stores
- Adding the data to Elasticsearch
- Compute Jaccard distance between datasets

Most of the code is written in python 3.8.6 and the scraping and adding to Elasticsearch has been done in Linux, more specifically on Ubuntu 20.10. Therefore, the documentation is based on the fact that we used Ubuntu, but similar commands may exist for Windows and MacOS.

For this project we have used:
- scrapy 2.4.1
- selenium 3.141.0
- elasticsearch 7.11.1
- kibana 7.11.1

Other dependencies:
- logzero 1.6.3
- numpy 1.19.2

Elasticsearch is based on java and therefore we need Open JDK 11 on our machine.

### References
We have used the following as inspiration for implementation and installation
- https://towardsdatascience.com/web-scraping-with-selenium-d7b6d8d3265a
- https://www.elastic.co/guide/en/elastic-stack-get-started/current/get-started-elastic-stack.html
- https://stackoverflow.com/questions/33980591/insert-multiple-documents-in-elasticsearch
- http://brandonrose.org/clustering

## Installations
We will briefly describe the installation of the packages. 

### Open JDK 11
Update package index:
```shell
$ sudo apt update
```
Install the default Java Runtime Environment (JRE), which will install the JRE from OpenJDK 11:
```shell
$ sudo apt install default-jre
```

### Elasticsearch
You can either download the most recent package from https://www.elastic.co/start or install directly from the terminal.
First the Elasticsearch must be added to the packages index
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
The second command ensures that Elasticsearch starts at systemboot. Elasticsearch runs by default on localhost:9200.

### Kibana
Install Kibana after Elasticsearch.
```shell
$ sudo apt install kibana
$ sudo systemctl enable kibana
$ sudo systemctl start kibana
```
Kibana will per default run on localhost:5601 (http://localhost:5601)

### Scrapy

### Selenium 
Installing selenium is easy on linux. 
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
First we create a scrapy project
```shell
$ 
```
In the scripts settings.py we enable AutoThrottle and set start delay to 5. This is done since **why?**
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
Afterwards the datascraping spiders are run by 
```shell
/main/copernicus_scrape$ scrapy crawl CDSScrapeSpider -o data/CDS_data.json 
/main/copernicus_scrape$ scrapy crawl ADSScrapeSpider -o data/ADS_data.json 
```

## Adding data to Elasticsearch
In order to add the data to Elasticsearch we use the bulk API. This is described in https://stackoverflow.com/questions/33980591/insert-multiple-documents-in-elasticsearch.
We use the scripts CDS_bulk.sh and ADS_bulk.sh to add the data to Elasticsearch. This is done by first editing the script and then running it:
```shell
/Elasticsearch$ nano ADS_bulk.sh
/Elasticsearch$ chmod u+x ADS_bulk.sh
/Elasticsearch$ ./ADS_bulk.sh
```

## Searching in Elasticsearch
Searching can be done either through the dev tools in Kibana or by using curl in the commandline. 

Search for "temperature" in the dev tool by writing:
```shell
GET /datasetname/_search?q=temperature
```

Search for temperature in the commandline using curl by writing:
```shell
curl -XGET "http:\\localhost:9200/datasetname/_search?q=temprature&pretty
```

## Compute Jaccard distance between webpages
In order to compute the Jaccard distance between the scraped webpages run the script Clustering/Jaccard_copernicus.py from the Python IDE of your choice. The functions used in Jaccard_copernicus.py can be found in Clustering/Module.py and are documented in the script.


[comment]: <> (git remote add origin https://github.com/ksagaa17/copernicus_data.git)

[comment]: <> (pull with git pull origin main)
