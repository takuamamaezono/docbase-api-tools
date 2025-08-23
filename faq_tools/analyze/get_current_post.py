#!/usr/bin/env python3
"""
DocBase記事の現在の内容を取得するスクリプト
"""

import requests
import json
import os

# 設定
TEAM_NAME = "go"
POST_ID = 2705590
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("エラー: DOCBASE_ACCESS_TOKEN が設定されていません")
    exit(1)

# APIリクエスト
url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{POST_ID}"
headers = {
    "X-DocBaseToken": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    post = response.json()
    
    print("=== 現在の記事情報 ===")
    print(f"タイトル: {post.get('title', 'N/A')}")
    print(f"作成日: {post.get('created_at', 'N/A')}")
    print(f"更新日: {post.get('updated_at', 'N/A')}")
    print(f"タグ: {', '.join([tag['name'] for tag in post.get('tags', [])])}")
    print(f"公開範囲: {post.get('scope', 'N/A')}")
    print("\n=== 本文 ===")
    print(post.get('body', ''))
    
    # 本文をファイルに保存
    with open('current_post_content.md', 'w', encoding='utf-8') as f:
        f.write(post.get('body', ''))
    print("\n本文を 'current_post_content.md' に保存しました")
    
except requests.exceptions.RequestException as e:
    print(f"エラーが発生しました: {e}")
    if hasattr(e, 'response') and hasattr(e.response, 'text'):
        print(f"詳細: {e.response.text}")