#!/bin/sh

ES_HOST=localhost:9200
cd ..
WD=$(pwd)
JSON_FILE_IN=$WD/copernicus_scrape/data/ADS_data.json
JSON_FILE_OUT=$WD/Elasticsearch/bulk_ADS_data.json

PYTHON="import json,sys;
out = open('$JSON_FILE_OUT', 'w');
with open('$JSON_FILE_IN') as json_in:
    docs = json.loads(json_in.read());
    i=0;
    for doc in docs:
        out.write('%s\\n' % json.dumps({'index': {'_id':'{}'.format(i)}}));
        out.write('%s\\n' % json.dumps(doc, indent=0).replace('\n', ' '));
        i += 1;
"

python3 -c "$PYTHON"

curl -s -XPOST $ES_HOST/copernicus7/_bulk -H 'Content-Type: application/json' --data-binary @$JSON_FILE_OUT
