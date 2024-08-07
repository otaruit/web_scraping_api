import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLを指定
url = "https://www.city.ebetsu.hokkaido.jp/site/kosodate/72891.html"

# Webページの内容を取得
response = requests.get(url)
response.raise_for_status()  # ステータスコードが200でない場合、例外を発生させる

# BeautifulSoupでHTMLを解析
soup = BeautifulSoup(response.text, 'html.parser')

# テーブルを取得
table = soup.find('table')



# テーブルをDataFrameに変換
df = pd.read_html(str(table))[0]
table_name = "やよい"  # 例: 保育園名を指定
filtered_df = df[df['保育園名'] == table_name]
print(filtered_df)
# DataFrameを表示

# 必要な情報だけを取得する場合（例: "やよい"という保育園名を持つテーブルを抽出する）

