import Modules as M
import json
import os

#%%CDS
pardir = os.path.dirname(os.getcwd())

with open(pardir+'/copernicus_scrape/CDS_data.json') as f:
  CDS = json.load(f)

# CDS_string = []
# N = len(CDS)
# for i in range(N):
#     tmp = json.dumps(CDS[i])
#     CDS_string.append(tmp)
    
CDS_string_preprocessed = M.Preprocessing(CDS)
Jaccard_matrix_CDS = M.jaccard_matrix(CDS_string_preprocessed)
near_CDS = M.nearest_docs(CDS, Jaccard_matrix_CDS, 95, 5)
near_thres_CDS = M.nearest_docs_thres(CDS, Jaccard_matrix_CDS, 0, 0.45)

#%%ADS
pardir = os.path.dirname(os.getcwd())

with open(pardir+'/copernicus_scrape/ADS_data.json') as f:
  ADS = json.load(f)

# ADS_string = []
# K = len(ADS)
# for i in range(K):
#     tmp = json.dumps(ADS[i])
#     ADS_string.append(tmp)

ADS_string_preprocessed = M.Preprocessing(ADS)
Jaccard_matrix_ADS = M.jaccard_matrix(ADS_string_preprocessed) 
near_ADS = M.nearest_docs(ADS, Jaccard_matrix_ADS, 2, 5)
near_thres_ADS = M.nearest_docs_thres(ADS, Jaccard_matrix_ADS, 0, 0.45)

#%% Both
# with open(pardir+'/copernicus_scrape/ADS_data.json') as f:
#     Combined = json.load(f)

# with open(pardir+'/copernicus_scrape/CDS_data.json') as g:
#     Combined.append(g)

# Combined_string = []
# for i in range(K):
#     tmp = json.dumps(ADS[i])
#     Combined_string.append(tmp)

# for i in range(N):
#     tmp = json.dumps(CDS[i])
#     Combined_string.append(tmp)

# Combined_string_preprocessed = M.Preprocessing(Combined_string)
# Jaccard_matrix_Combined = M.jaccard_matrix(Combined_string_preprocessed) 
# near_combined = M.nearest_docs(Combined, Jaccard_matrix_Combined, 2, 5)
# near_thres_Combined = M.nearest_docs_thres(Combined, Jaccard_matrix_Combined, 0, 0.45)

Jaccard_matrix_Combined = M.jaccard_matrix_update(Jaccard_matrix_ADS, 
                                                  ADS_string_preprocessed, CDS_string_preprocessed)
near_ADS = M.nearest_docs(ADS, Jaccard_matrix_ADS, 2, 5)
near_thres_ADS = M.nearest_docs_thres(ADS, Jaccard_matrix_ADS, 0, 0.45)
