#!/usr/bin/env python3
"""
DocBase記事を直接更新するスクリプト
"""

import requests
import os

# 設定
TEAM_NAME = "go"
POST_ID = 2705590
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("エラー: DOCBASE_ACCESS_TOKEN が設定されていません")
    exit(1)

# フォーマット済みの内容を読み込む
print("フォーマット済みの内容を読み込んでいます...")
with open('formatted_post_content.md', 'r', encoding='utf-8') as f:
    new_body = f.read()

# 更新を実行
url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{POST_ID}"
headers = {
    "X-DocBaseToken": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

update_data = {
    "body": new_body
}

print(f"記事ID {POST_ID} を更新しています...")
try:
    response = requests.patch(url, headers=headers, json=update_data)
    response.raise_for_status()
    print("✅ 記事の更新に成功しました！")
    print(f"更新日時: {response.json().get('updated_at', 'N/A')}")
    print(f"URL: https://go.docbase.io/posts/{POST_ID}")
except requests.exceptions.RequestException as e:
    print(f"❌ 記事の更新に失敗しました: {e}")
    if hasattr(e.response, 'text'):
        print(f"エラー詳細: {e.response.text}")