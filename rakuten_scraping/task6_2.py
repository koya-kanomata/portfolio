import requests
import numpy as np
import pandas as pd

url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
app_id = "1021298500308407354"

serch_keyword = '腕時計'

serch_params={
    "format" : "json",
    "keyword" : serch_keyword,
    "applicationId" : app_id,
    "availability" : 0,
    "hits" : 30,
    "page" : 1,
    "sort" : "standard"
}

response = requests.get(url, serch_params)
result = response.json()

#print(result)

item_key = ['itemName', 'itemPrice']
item_list = []
for i in range(0, len(result['Items'])):
    tmp_item = {}
    item = result['Items'][i]['Item']
    for key, value in item.items():
        if key in item_key:
            tmp_item[key] = value
    item_list.append(tmp_item.copy())

print(item_list)
