
import pandas as pd

# WikipediaのURL
url = 'https://www.city.ebetsu.hokkaido.jp/site/kosodate/72891.html'

# マッチするテーブルを取得する関数
def get_nursary_info(match_string):
    df_list = pd.read_html(url, match=match_string)
    if df_list:
        df = df_list[0]
        # 列名を確認
        print(f"テーブル '{match_string}' の列名:", df.columns)
        nursary_info_list = []
        for index, row in df.iterrows():
            # availabilityの辞書を動的に作成
            availability = {}
            for column in df.columns[1:]:  # 最初の列は名前の列なのでスキップ
                availability[column] = row[column]

            # 辞書型に変換
            nursary_info = {
                "nursary_name": row[df.columns[0]],
                "availability": availability
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
