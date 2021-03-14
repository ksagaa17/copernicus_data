# Copernicus Data

## Introduction
This is the code and data used for scraping the Copernicus datastors *Atmosphere Data Store* and *Climate Data Store*. These are found here:
- https://ads.atmosphere.copernicus.eu/cdsapp#!/search?type=dataset
- https://cds.climate.copernicus.eu/cdsapp#!/search?type=dataset

The project includes 
- Scraping the data stores
- Adding the data to Elasticsearch
- Compute Jaccard Distance between datasets

Most of the code is written in python 3.8.6 and the scraping and adding to Elasticsearch has been done in Linux, more specifically on Ubuntu 20.10. Therefore, the documentation is based on the fact that we used Ubuntu, but similar commands may exists for Windows and MacOS.

For this project we have used:
- scrapy 2.4.1  
- selenium 3.141.0  
- elasticsearch 7.11.1
- kibana 7.11.1

Other dependencies:
- logzero 1.6.3 
- numpy 1.19.2

Elasticsearch is based on java and therefore we need Open JDK 11 on our machine. 

## Installations
We will breifly descripe the installation of the pakages. 

### Open JDK 11
```shell
$ sudo apt update
```

git remote add origin https://github.com/ksagaa17/copernicus_data.git

pull with git pull origin main
