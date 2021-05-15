import csv
import eel
import requests
import numpy as np
import pandas as pd
import datetime
import os

csv_file = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\')+'result_{}.csv'.format(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
print(csv_file)

def search_item(max,word):
    max=int(max)
    eel.view_log_js("検索開始")
    item_list = []
    for i in range(1,):
        url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
        app_id = "1021298500308407354"

        search_keyword = word

        search_params={
            "format" : "json",
            "keyword" : search_keyword,
            "applicationId" : app_id,
            "availability" : 0,
            "hits" : 30,
            "page" : i,
            "sort" : "standard"
        }
        response = requests.get(url, search_params)
        result = response.json()

        item_key = ['itemName', 'itemPrice']
        for i in range(0, len(result['Items'])):
            tmp_item = {}
            item = result['Items'][i]['Item']
            for key, value in item.items():
                if key in item_key:
                    tmp_item[key] = value
            item_list.append(tmp_item.copy())
    print(item_list)

#CSV出力
    df = pd.DataFrame(item_list)
    df.to_csv(csv_file,encoding='utf-8')
    

    eel.view_log_js("検索完了")
    eel.view_log_js("CSVファイル:{}".format(csv_file))

