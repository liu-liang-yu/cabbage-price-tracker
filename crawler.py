# crawler.py

import requests
import pandas as pd
from io import StringIO
from datetime import datetime

def fetch_cabbage_price():
    url = 'https://data.moa.gov.tw/Service/OpenData/FromM/AgricultureiRiceData.aspx'
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))

        # 選取包含「高麗菜」的資料（你可根據實際欄位名稱微調）
        cabbage_df = df[df['作物名稱'].str.contains('高麗菜', na=False)]

        # 取最新一筆（假設依照日期排序）
        latest = cabbage_df.sort_values('交易日期', ascending=False).head(1)

        if not latest.empty:
            price = float(latest.iloc[0]['平均價'])  # 平均價欄位
            date = latest.iloc[0]['交易日期']
            return date, price
        else:
            return None, None

    except Exception as e:
        print("錯誤：", e)
        return None, None
