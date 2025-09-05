#!/usr/bin/env python3

import os
import requests
import json
from datetime import datetime

# 環境変数を読み込む
def load_env_from_file():
    env_path = '/Users/g.ohorudingusu/Docbase/.env'
    with open(env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

load_env_from_file()

# 設定
API_TOKEN = os.getenv('DOCBASE_ACCESS_TOKEN')
TEAM = os.getenv('DOCBASE_TEAM')

# 記事ファイルの読み込み
article_file = '/Users/g.ohorudingusu/Docbase/illustrator_search_plugin_guide.md'
with open(article_file, 'r', encoding='utf-8') as f:
    content = f.read()

# APIエンドポイント
url = f"https://api.docbase.io/teams/{TEAM}/posts"

# ヘッダー
headers = {
    'X-DocBase-Token': API_TOKEN,
    'Content-Type': 'application/json'
}

# データ
data = {
    'title': 'Adobe Illustrator Search Plugin - Hammerspoon実装ガイド',
    'body': content,
    'draft': False,
    'scope': 'private',  # 従業員のみ
    'tags': ['Hammerspoon', 'Adobe Illustrator', 'macOS', 'プラグイン', '効率化ツール']
}

print("記事をアップロード中...")
response = requests.post(url, headers=headers, json=data)

print(f"ステータスコード: {response.status_code}")
if response.status_code == 201:
    result = response.json()
    print(f"✅ 記事作成完了！")
    print(f"記事ID: {result['id']}")
    print(f"URL: {result['url']}")
    
    # 結果を保存
    with open(f'illustrator_plugin_result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        
else:
    print(f"❌ エラー: {response.text}")