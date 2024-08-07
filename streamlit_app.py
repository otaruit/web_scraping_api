import pandas as pd
import streamlit as st
import requests

# WikipediaのURL
url = 'https://www.city.ebetsu.hokkaido.jp/site/kosodate/72891.html'

# LINE Notifyのアクセストークン
LINE_NOTIFY_TOKEN = ''  # ここにアクセストークンを入力

# マッチするテーブルを取得する関数
def get_nursary_info(match_string):
    df_list = pd.read_html(url, match=match_string)
    if df_list:
        df = df_list[0]
        nursary_info_list = []
        for index, row in df.iterrows():
            # availabilityの辞書を動的に作成
            availability = {}
            for column in df.columns[1:]:  # 最初の列は名前の列なのでスキップ
                availability[column] = row[column]

            # 辞書型に変換
            nursary_info = {
                "nursary_name": row[df.columns[0]],
                **availability  # availabilityを直接展開して追加
            }
            nursary_info_list.append(nursary_info)
        return nursary_info_list
    else:
        return []

# 各テーブルの情報を取得
childcare = get_nursary_info('【公立】やよい')
community_childcare = get_nursary_info('あすかの森')
certified_childcare = get_nursary_info('ぞうさんハウス')

# 年齢と対応状況の選択肢
age_options = ['０歳', '１歳', '２歳', '３歳', '４歳', '５歳']
availability_options = ['〇', '△', '☓']

# Streamlitアプリケーションの設定
st.title('保育園情報')

# セッション状態の初期化
if 'selected_age' not in st.session_state:
    st.session_state.selected_age = age_options[0]
if 'selected_availability' not in st.session_state:
    st.session_state.selected_availability = availability_options[0]

# ユーザーの選択を取得
selected_age = st.selectbox('年齢を選択:', age_options, index=age_options.index(st.session_state.selected_age))
selected_availability = st.selectbox('対応状況を選択:', availability_options, index=availability_options.index(st.session_state.selected_availability))

# セッション状態に保存
st.session_state.selected_age = selected_age
st.session_state.selected_availability = selected_availability

# テーブルを表示する関数
def display_filtered_table(data, age, availability):
    st.write(f"フィルタリング条件 - 年齢: {age}, 対応状況: {availability}")
    filtered_data = [entry for entry in data if entry.get(age) == availability]
    
    if filtered_data:
        df = pd.DataFrame(filtered_data)
        st.dataframe(df)  # または st.table(df) でも良い
        return df
    else:
        st.write("条件に一致するデータがありません")
        return None

# 各カテゴリのテーブルを表示
st.header('Childcare')
df_childcare = display_filtered_table(childcare, selected_age, selected_availability)

st.header('Community Childcare')
df_community_childcare = display_filtered_table(community_childcare, selected_age, selected_availability)

st.header('Certified Childcare')
df_certified_childcare = display_filtered_table(certified_childcare, selected_age, selected_availability)

# ドロップダウンリストの直下に「LINEで通知」ボタンと「保存」ボタンを配置
col1, col2 = st.columns([2, 1])

with col1:
    if st.button('LINEで通知'):
        message = f'年齢: {selected_age}, 対応状況: {selected_availability}\n'
        message += 'フィルタリングされたデータ:\n'
        
        # フィルタリングされたデータをメッセージに追加
        for df in [df_childcare, df_community_childcare, df_certified_childcare]:
            if df is not None:
                for index, row in df.iterrows():
                    row_message = f"{row['nursary_name']}: " + ', '.join([f"{col}: {row[col]}" for col in df.columns if col != 'nursary_name'])
                    message += row_message + '\n'
        
        # LINEにメッセージを送信
        response = send_line_notify(message)
        
        if response.status_code == 200:
            st.success('LINEに通知が送信されました。')
        else:
            st.error('LINEへの通知に失敗しました。')

with col2:
    if st.button('保存'):
        # セッション状態の選択肢をファイルに保存
        with open('selected_options.txt', 'w') as file:
            file.write(f"選択された年齢: {st.session_state.selected_age}\n")
            file.write(f"選択された対応状況: {st.session_state.selected_availability}\n")
        st.success('選択肢が保存されました。')

# LINE Notifyで通知する関数
def send_line_notify(message):
    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {'message': message}
    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload)
    return response
