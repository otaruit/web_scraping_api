




import pandas as pd

# WikipediaのURL
url = 'https://www.city.ebetsu.hokkaido.jp/site/kosodate/72891.html'

# 日本語版にマッチするテーブルを取得
df_list = pd.read_html(url, match='【公立】やよい')

# テーブルが見つかった場合、最初のテーブルを取得
if df_list:
    df = df_list[0]
    
    # 各行を表示
    for index, row in df.iterrows():
        print(row)
else:
    print("指定したテーブルが見つかりませんでした。")
