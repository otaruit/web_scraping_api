import pandas as pd
import streamlit as st
import requests
import json
import shutil
import os
from datetime import datetime


st.set_page_config(page_title="江別市ほいくえんアプリ")

url = 'https://www.city.ebetsu.hokkaido.jp/site/kosodate/72891.html'

def load_env_vars():
    if not os.path.exists('env.json'):
        if os.path.exists('env.json.sample.json'):
            shutil.copy('env.json.sample.json', 'env.json')
            st.warning('env.json.sample.jsonからenv.jsonを作成しました。適切な値に更新してください。')
        else:
            st.error('env.json ファイルが見つかりません')
            return ''
    
    try:
        with open('env.json', 'r') as f:
            env = json.load(f)
            return env.get('LINE_NOTIFY_TOKEN', '')
    except json.JSONDecodeError:
        st.error('env.json の形式が不正です')
        return ''

LINE_NOTIFY_TOKEN = load_env_vars()

def send_line_notify(message):
    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {'message': message}
    response = requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload)
    return response

def get_nursary_info(match_string):
    df_list = pd.read_html(url, match=match_string)
    if df_list:
        df = df_list[0]
        nursary_info_list = []
        for index, row in df.iterrows():
            availability = {}
            for column in df.columns[1:]:
                availability[column] = row[column]

            nursary_info = {
                "施設名": row[df.columns[0]],
                **availability
            }
            nursary_info_list.append(nursary_info)
        return nursary_info_list
    else:
        return []

childcare = get_nursary_info('【公立】やよい')
community_childcare = get_nursary_info('あすかの森')
certified_childcare = get_nursary_info('ぞうさんハウス')

age_options = ['０歳', '１歳', '２歳', '３歳', '４歳', '５歳']
availability_options = ['〇', '△', '☓']


current_month = str(int(datetime.now().strftime('%m'))) 
st.title(f'江別市保育園{current_month}月の入所状況')

st.write("〇：空きあり　△：若干空きあり　☓：空きなし")

if 'selected_age' not in st.session_state:
    st.session_state.selected_age = age_options[0]
if 'selected_availability' not in st.session_state:
    st.session_state.selected_availability = availability_options[0]

selected_age = st.selectbox('年齢を選択:', age_options, index=age_options.index(st.session_state.selected_age))
selected_availability = st.selectbox('対応状況を選択:', availability_options, index=availability_options.index(st.session_state.selected_availability))

st.session_state.selected_age = selected_age
st.session_state.selected_availability = selected_availability

col1, col2 = st.columns([2, 1])

def display_filtered_table(data, age, availability):
    st.write(f"条件 - 年齢: {age}, 対応状況: {availability}")
    filtered_data = [entry for entry in data if entry.get(age) == availability]
    
    if filtered_data:
        df = pd.DataFrame(filtered_data)
        st.dataframe(df)
        return df
    else:
        st.write("条件に一致するデータがありません")
        return None

st.header('保育所')
df_childcare = display_filtered_table(childcare, selected_age, selected_availability)

st.header('認定こども園')
df_community_childcare = display_filtered_table(community_childcare, selected_age, selected_availability)

st.header('地域型保育')
df_certified_childcare = display_filtered_table(certified_childcare, selected_age, selected_availability)

with col1:
    if st.button('LINEで通知'):
        message = f'年齢: {st.session_state.selected_age}, 対応状況: {st.session_state.selected_availability}\n'
        message += 'フィルタリングされたデータ:\n'
        
        for df in [df_childcare, df_community_childcare, df_certified_childcare]:
            if df is not None:
                for index, row in df.iterrows():
                    row_message = f"{row['施設名']}: " + ', '.join([f"{col}: {row[col]}" for col in df.columns if col != '施設名'])
                    message += row_message + '\n'
        
        response = send_line_notify(message)
        
        if response.status_code == 200:
            st.success('LINEに通知が送信されました。')
        else:
            st.error('LINEへの通知に失敗しました。')

with col2:
    if st.button('選択内容を保存'):
        with open('selected_options.txt', 'w') as file:
            file.write(f"選択された年齢: {st.session_state.selected_age}\n")
            file.write(f"選択された対応状況: {st.session_state.selected_availability}\n")
        st.success('選択肢が保存されました。')
