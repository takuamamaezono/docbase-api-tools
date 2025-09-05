#!/usr/bin/env python3
"""
Docbase古い記事警告システムのマニュアルをDocbaseに投稿するスクリプト
"""

import requests
import os
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# 設定
TEAM_NAME = os.getenv("DOCBASE_TEAM", "go")
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("エラー: DOCBASE_ACCESS_TOKEN が設定されていません")
    exit(1)

# マニュアル内容を読み込む
print("マニュアル内容を読み込んでいます...")
with open('docbase_old_article_warning/QUICK_EXECUTION_GUIDE.md', 'r', encoding='utf-8') as f:
    body_content = f.read()

# 新規記事作成データ
article_data = {
    "title": "【システム】Docbase古い記事への注意書き追加 - 実行ガイド",
    "body": body_content,
    "draft": False,
    "scope": "private",  # 従業員のみ（G.O / 加島）
    "tags": [
        "Docbase",
        "システム運用",
        "古い記事",
        "注意書き",
        "自動化",
        "メンテナンス",
        "API"
    ]
}

# Docbase APIに記事を作成
url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts"
headers = {
    "X-DocBaseToken": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

print("Docbaseに古い記事警告システムの実行ガイドを投稿中...")
try:
    response = requests.post(url, headers=headers, json=article_data)
    response.raise_for_status()
    
    result = response.json()
    print("✅ 記事の作成に成功しました！")
    print(f"記事ID: {result.get('id')}")
    print(f"記事タイトル: {result.get('title')}")
    print(f"URL: {result.get('url')}")
    print(f"作成日時: {result.get('created_at')}")
    
except requests.exceptions.RequestException as e:
    print(f"❌ 記事の作成に失敗しました: {e}")
    if hasattr(e, 'response') and e.response:
        print(f"ステータスコード: {e.response.status_code}")
        print(f"エラー詳細: {e.response.text}")