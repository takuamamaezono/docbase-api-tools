#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerArQ チャットボット自動テストシステムの記事をDocbaseに投稿
"""

import os
import requests
import json
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# 環境変数から設定を取得
API_TOKEN = os.getenv('DOCBASE_ACCESS_TOKEN')
TEAM = os.getenv('DOCBASE_TEAM')

# TEAMを直接設定（.envから読み込み、なければデフォルト値）
if not TEAM:
    TEAM = "go"

if not API_TOKEN:
    print("❌ 環境変数が設定されていません")
    print("DOCBASE_ACCESS_TOKEN を設定してください")
    exit(1)

# 記事内容を読み込み
with open('/Users/g.ohorudingusu/Docbase/chatbot_test_article.md', 'r', encoding='utf-8') as f:
    article_content = f.read()

# Docbase APIエンドポイント
url = f"https://api.docbase.io/teams/{TEAM}/posts"

headers = {
    'X-DocBaseToken': API_TOKEN,
    'Content-Type': 'application/json'
}

# 投稿データ
data = {
    "title": "PowerArQ チャットボット自動テストシステム",
    "body": article_content,
    "draft": False,  # 公開状態
    "scope": "private",  # 従業員のみ
    "tags": ["システム", "チャットボット", "テスト", "自動化", "PowerArQ", "API"]
}

try:
    print("📝 Docbaseに記事を投稿中...")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        result = response.json()
        print("✅ 記事の投稿に成功しました！")
        print(f"📄 記事タイトル: {result['title']}")
        print(f"🔗 記事URL: {result['url']}")
        print(f"📅 作成日時: {result['created_at']}")
        print(f"🏷️ タグ: {', '.join([tag['name'] for tag in result['tags']])}")
    else:
        print(f"❌ 記事の投稿に失敗しました")
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.text}")

except Exception as e:
    print(f"❌ エラーが発生しました: {e}")