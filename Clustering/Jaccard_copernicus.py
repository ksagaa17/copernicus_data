import Modules as M
import json


with open('copernicus_scrape/CDS_data.json') as f:
  CDS = json.load(f)

CDS_string = []
N = len(CDS)
for i in range(N):
    tmp = json.dumps(CDS[i])
    CDS_string.append(tmp)

with open('copernicus_scrape/ADS_data.json') as f:
  ADS = json.load(f)

ADS_string = []
K = len(ADS)
for i in range(K):
    tmp = json.dumps(ADS[i])
    ADS_string.append(tmp)

ADS_string_preprocessed = M.Preprocessing(ADS_string)
Jaccard_matrix_ADS = M.jaccard_matrix(ADS_string_preprocessed) 

CDS_string_preprocessed = M.Preprocessing(CDS_string)
Jaccard_matrix_CDS = M.jaccard_matrix(CDS_string_preprocessed)
 