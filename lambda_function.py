import json
import boto3
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

s3 = boto3.resource('s3')

def get_h3_with_images(class_name_h3, class_name_img, url):
    print(f"このURLからウェブスクレイピング実行中: {url}")
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
    
    print(f" {len(result)} 個のイベントタイトルを取得.")
    return result


def get_event_details(url):
    print(f"このURLのイベント詳細情報を取得: {url}")
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    details_list = []
    
    events = soup.find_all('div', class_='event_detail')  
    
    for event in events:
        details = {}
        

        start_time = event.find('div', class_='col left', string='開催時期')
        if start_time:
            details['開催時期'] = start_time.find_next_sibling('div').get_text(strip=True)

        end_time = event.find('div', class_='col left', string='終了時期')
        if end_time:
            details['終了時期'] = end_time.find_next_sibling('div').get_text(strip=True)

        location = event.find('div', class_='col left', string='場所')
        if location:
            details['場所'] = location.find_next_sibling('div').get_text(strip=True)
        
        details_list.append(details)
    
    print(f"Found details for {len(details_list)} events.")
    return details_list


def lambda_handler(event, context):
    print("ラムダ関数実行開始")
    
    current_month = datetime.now().month
    if 3 <= current_month <= 5:
        season = 'spring'
    elif 6 <= current_month <= 8:
        season = 'summer'
    elif 9 <= current_month <= 11:
        season = 'fall'
    else:
        season = 'winter'

    url = f'https://otaru.gr.jp/{season}'
    print(f"季節の設定ワード: {season}")

    class_name_h3 = 'head_item event_title'
    class_name_img = 'attachment-3x2 size-3x2 wp-post-image'

    h3_with_images = get_h3_with_images(class_name_h3, class_name_img, url)
    event_details = get_event_details(url)

    events = []
    if h3_with_images and event_details:
        for i in range(min(len(h3_with_images), len(event_details))):
            events.append({
                "title": h3_with_images[i]['title'],
                "img_src": h3_with_images[i]['img_src'],
                "details": event_details[i]
            })
    
    print(f"S3に {len(events)} 個のイベントを保存する準備開始")

    file_contents = json.dumps(events, ensure_ascii=False)
    bucket = 'apibukket'
    key = 'event_data_' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.json'
    s3_object = s3.Object(bucket, key)
    response = s3_object.put(Body=file_contents)
    
    print(f"右の名前でS3に保存完了: {key}")

    return {
        'statusCode': 200,
        'body': json.dumps({"message": "S3へのアップロード完了", "key": key}, ensure_ascii=False)
    }
