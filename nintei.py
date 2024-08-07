
import pandas as pd

# WikipediaのURL
url = 'https://www.city.ebetsu.hokkaido.jp/site/kosodate/72891.html'

# 日本語版にマッチするテーブルを取得
df_list = pd.read_html(url, match='あすかの森')

# テーブルが見つかった場合、最初のテーブルを取得
if df_list:
    df = df_list[0]

    # 各行を辞書型に変換してリストにまとめる
    nursary_info_list = []

    for index, row in df.iterrows():
        # 辞書型に変換
        nursary_info = {
            "nursary_name": row["Unnamed: 0"],
            "availability": {
                "０歳": row["０歳"],
                "１歳": row["１歳"],
                "２歳": row["２歳"],
                "３歳": row["３歳"],
                "４歳": row["４歳"],
                "５歳": row["５歳"]
            }
        }
        nursary_info_list.append(nursary_info)

    # 結果を表示
    for nursary_info in nursary_info_list:
        print(nursary_info)
else:
    print("指定したテーブルが見つかりませんでした。")