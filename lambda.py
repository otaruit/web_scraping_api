import json
import requests
from bs4 import BeautifulSoup
import urllib3
from flask import Flask, jsonify

# Flaskアプリケーションの作成
app = Flask(__name__)

# 警告を無視する設定
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

@app.route('/api/events', methods=['GET'])
def get_events():
    class_name_h3 = 'head_item event_title'
    class_name_img = 'attachment-3x2 size-3x2 wp-post-image'

    h3_with_images = get_h3_with_images(class_name_h3, class_name_img)
    event_details = get_event_details()

    events = []
    if h3_with_images and event_details:
        for i in range(min(len(h3_with_images), len(event_details))):
            events.append({
                "title": h3_with_images[i]['title'],
                "img_src": h3_with_images[i]['img_src'],
                "details": event_details[i]
            })
    
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
