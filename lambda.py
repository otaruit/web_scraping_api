import requests
from bs4 import BeautifulSoup
import streamlit as st
import urllib3

# 警告を無視する設定
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="イベント情報")
st.write("https://otaru.gr.jp/summer からWEBスクレイピング")

url = 'https://otaru.gr.jp/summer'

# h3タグと画像を取得する関数
def get_h3_with_images(class_name_h3, class_name_img):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    h3_tags = soup.find_all('h3', class_=class_name_h3)
    
    result = []
    for h3 in h3_tags:
        img_tag = h3.find_next('img', class_=class_name_img)
        img_src = img_tag['src'] if img_tag else None
        
        result.append({
            "title": h3.get_text(strip=True),
            "img_src": img_src
        })
    
    return result

# イベント詳細情報を取得する関数
def get_event_details():
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    details_list = []
    
    events = soup.find_all('div', class_='event_detail')  # 各イベントの詳細が格納された要素を取得
    
    for event in events:
        details = {}
        
        # 開催時期を取得
        start_time = event.find('div', class_='col left', string='開催時期')
        if start_time:
            details['開催時期'] = start_time.find_next_sibling('div').get_text(strip=True)
        
        # 終了時期を取得
        end_time = event.find('div', class_='col left', string='終了時期')
        if end_time:
            details['終了時期'] = end_time.find_next_sibling('div').get_text(strip=True)
        
        # 場所を取得
        location = event.find('div', class_='col left', string='場所')
        if location:
            details['場所'] = location.find_next_sibling('div').get_text(strip=True)
        
        details_list.append(details)
    
    return details_list

# h3タグと画像、イベント詳細情報を取得
class_name_h3 = 'head_item event_title'
class_name_img = 'attachment-3x2 size-3x2 wp-post-image'

h3_with_images = get_h3_with_images(class_name_h3, class_name_img)
event_details = get_event_details()

# 結果をStreamlitで表示
if h3_with_images and event_details:
    for i in range(min(len(h3_with_images), len(event_details))):
        st.write("タイトル:", h3_with_images[i]['title'])
        if h3_with_images[i]['img_src']:
            st.image(h3_with_images[i]['img_src'])  # 画像を表示
        else:
            st.write("画像が見つかりませんでした。")
        
        # イベントの詳細情報を表示
        details = event_details[i]
        st.write("開催時期:", details.get('開催時期', '情報がありません'))
        st.write("終了時期:", details.get('終了時期', '情報がありません'))
        st.write("場所:", details.get('場所', '情報がありません'))
        st.write("---")
else:
    st.write("指定されたクラスの<h3>タグやイベント詳細情報が見つかりませんでした。")
