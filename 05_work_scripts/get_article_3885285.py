#!/usr/bin/env python3
"""
記事ID 3885285の内容を取得するスクリプト
"""

import requests
import json
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

def get_article(team_name, access_token, post_id):
    """
    記事の内容を取得
    """
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/teams/{team_name}/posts/{post_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"記事の取得に失敗しました: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"レスポンス: {e.response.text}")
        return None

def main():
    # 記事ID 3885285を取得
    TEAM_NAME = "go"
    POST_ID = 3885285
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        print("APIトークンを設定してください")
        return
    
    print(f"記事ID {POST_ID} の内容を取得中...")
    article = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if article:
        print("=== 記事情報 ===")
        print(f"タイトル: {article.get('title', 'N/A')}")
        print(f"作成日: {article.get('created_at', 'N/A')}")
        print(f"更新日: {article.get('updated_at', 'N/A')}")
        print(f"タグ: {', '.join([tag['name'] for tag in article.get('tags', [])])}")
        print(f"公開範囲: {article.get('scope', 'N/A')}")
        print(f"本文の文字数: {len(article.get('body', ''))}")
        
        # 本文をMarkdownファイルに保存
        with open('/Users/g.ohorudingusu/Work/Docbase/article_3885285_body.md', 'w', encoding='utf-8') as f:
            f.write(article.get('body', ''))
        print("\n記事の本文を article_3885285_body.md に保存しました")
        
        # JSONファイルに保存
        with open('/Users/g.ohorudingusu/Work/Docbase/article_3885285_backup.json', 'w', encoding='utf-8') as f:
            json.dump(article, f, ensure_ascii=False, indent=2)
        print("記事の全データを article_3885285_backup.json に保存しました")
    else:
        print("記事を取得できませんでした")

if __name__ == "__main__":
    main()