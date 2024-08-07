# import pandas as pd

# # WikipediaのURL
# url = 'https://www.city.ebetsu.hokkaido.jp/site/kosodate/72891.html'

# # 日本語版にマッチするテーブルを取得
# df_list = pd.read_html(url, match='【公立】やよい')

# print(df_list[0])







# import pandas as pd

# # WikipediaのURL
# url = 'https://www.city.ebetsu.hokkaido.jp/site/kosodate/72891.html'

# # 日本語版にマッチするテーブルを取得
# df_list = pd.read_html(url, match='【公立】やよい')

# # テーブルが見つかった場合、最初のテーブルを取得
# if df_list:
#     df = df_list[0]
    
#     # 各行を表示
#     for index, row in df.iterrows():
#         print(row)
# else:
#     print("指定したテーブルが見つかりませんでした。")



import pandas as pd

# WikipediaのURL
url = 'https://www.city.ebetsu.hokkaido.jp/site/kosodate/72891.html'

# マッチするテーブルを取得する関数
def get_nursary_info(match_string):
    df_list = pd.read_html(url, match=match_string)
    if df_list:
        df = df_list[0]
        nursary_info_list = []
        for index, row in df.iterrows():
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
        return nursary_info_list
    else:
        print(f"指定したテーブル '{match_string}' が見つかりませんでした。")
        return []

# 各テーブルの情報を取得
childcare = get_nursary_info('【公立】やよい')
community_childcare = get_nursary_info('あすかの森')
certified_childcare = get_nursary_info('ぞうさんハウス')

# 結果を表示
print("Childcare:")
for info in childcare:
    print(info)

print("\nCommunity Childcare:")
for info in community_childcare:
    print(info)

print("\nCertified Childcare:")
for info in certified_childcare:
    print(info)
