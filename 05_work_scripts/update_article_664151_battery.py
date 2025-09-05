#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

def update_article():
    """記事を更新する"""
    
    # 環境変数から設定を取得
    api_token = os.getenv('DOCBASE_ACCESS_TOKEN') or os.getenv('DOCBASE_API_TOKEN')
    team = os.getenv('DOCBASE_TEAM', 'go')
    article_id = '664151'
    
    if not api_token:
        print("エラー: DOCBASE_API_TOKENが設定されていません")
        return False
    
    # APIエンドポイント
    url = f"https://api.docbase.io/teams/{team}/posts/{article_id}"
    
    # 現在の記事内容を取得
    headers = {
        'X-DocBaseToken': api_token,
        'Content-Type': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"記事の取得に失敗しました: {response.status_code}")
        return False
    
    article = response.json()
    current_body = article['body']
    
    # 29L・45L専用バッテリーの項目を探して更新
    # 現在の内容（\r\nを含む）
    old_section = """## ■ICEBERG 29L・45L専用バッテリー\r\n\r\n| 日付 | SKU | 納品数量 | ロットNo. | 備考 |\r\n| --- | --- | --- | --- | --- |\r\n| 2023年3月 | l0960 | 100個 | [APST001 ](https://app.asana.com/0/1109194477454509/1203172334432411/f)| 初回納品  |\r\n| 2023年9月 |l0960  |200  |[APST002](https://app.asana.com/0/1109194477454509/1205168138995641/f)  |  |\r\n| 2024年8月 | l0960 | 204 |[ TFST006](https://app.asana.com/0/inbox/1200135573634736/1207731873712192/1207820156677397) |製品モデル： TF01-3S6P<br>定格電圧： 10.8V<br>定格容量： 15.6Ah<br>容量： 168.48Wh<br>充電制限電圧： 12.6V<br>規格： GB 31241-2014 3INR19/66-6<br>製造国： 中国  |\r\n| 2025年5月 |l0960  | 504  |[TFST008](https://app.asana.com/1/789671625688551/project/1109194477454509/task/1209422007159586?focus=true)  |  |"""
    
    # 更新後の内容（充電仕様を追加）
    new_section = """## ■ICEBERG 29L・45L専用バッテリー\r\n\r\n| 日付 | SKU | 納品数量 | ロットNo. | 備考 |\r\n| --- | --- | --- | --- | --- |\r\n| 2023年3月 | l0960 | 100個 | [APST001 ](https://app.asana.com/0/1109194477454509/1203172334432411/f)| 初回納品  |\r\n| 2023年9月 |l0960  |200  |[APST002](https://app.asana.com/0/1109194477454509/1205168138995641/f)  |  |\r\n| 2024年8月 | l0960 | 204 |[ TFST006](https://app.asana.com/0/inbox/1200135573634736/1207731873712192/1207820156677397) |製品モデル： TF01-3S6P<br>定格電圧： 10.8V<br>定格容量： 15.6Ah<br>容量： 168.48Wh<br>充電制限電圧： 12.6V<br>規格： GB 31241-2014 3INR19/66-6<br>製造国： 中国  |\r\n| 2025年5月 |l0960  | 504  |[TFST008](https://app.asana.com/1/789671625688551/project/1109194477454509/task/1209422007159586?focus=true)  |  |\r\n\r\n### 充電仕様\r\n**45L側のバッテリー：**\r\n10.8V(MAX12.6V)/2A(MAX3A)\r\n\r\n**29L側のバッテリー：**\r\n10.8V(MAX12.6V)/2A(MAX3A)"""
    
    # 本文を更新
    updated_body = current_body.replace(old_section, new_section)
    
    if updated_body == current_body:
        print("警告: セクションが見つからなかったため、記事の更新をスキップしました")
        return False
    
    # 更新リクエストを送信
    # グループIDのリストを作成
    group_ids = [group['id'] for group in article.get('groups', [])]
    
    update_data = {
        'title': article['title'],
        'body': updated_body,
        'tags': article['tags'],
        'scope': 'group',  # 明示的にgroupを指定
        'groups': group_ids  # グループIDのリストを追加
    }
    
    response = requests.patch(url, headers=headers, json=update_data)
    
    if response.status_code == 200:
        print(f"✅ 記事ID {article_id} を正常に更新しました")
        print("追加内容: 29L・45L専用バッテリーの充電仕様")
        return True
    else:
        print(f"❌ 更新に失敗しました: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    update_article()