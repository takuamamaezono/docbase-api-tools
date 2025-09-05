#!/usr/bin/env python3
"""
記事ID 3885285を更新するスクリプト
"""

import requests
import json
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

def update_article(team_name, access_token, post_id, title, body, scope="private"):
    """
    記事を更新する
    """
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/teams/{team_name}/posts/{post_id}"
    
    data = {
        "title": title,
        "body": body,
        "scope": scope
    }
    
    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"記事の更新に失敗しました: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"レスポンス: {e.response.text}")
        return None

def main():
    # 環境変数を取得
    TEAM_NAME = "go"
    POST_ID = 3885285
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        print("APIトークンを設定してください")
        return
    
    # 更新する記事の内容を読み込む
    with open('/Users/g.ohorudingusu/Work/Docbase/article_3885285_updated.md', 'r', encoding='utf-8') as f:
        body = f.read()
    
    title = "Raycastの使い方"
    
    print(f"記事ID {POST_ID} を更新中...")
    result = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, title, body)
    
    if result:
        print("記事を更新しました！")
        print(f"タイトル: {result.get('title')}")
        print(f"更新日時: {result.get('updated_at')}")
        print(f"URL: https://go.docbase.io/posts/{POST_ID}")
    else:
        print("記事の更新に失敗しました")

if __name__ == "__main__":
    main()