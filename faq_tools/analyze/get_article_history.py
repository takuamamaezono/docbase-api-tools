#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数の設定
API_TOKEN = os.getenv('DOCBASE_ACCESS_TOKEN')
TEAM = os.getenv('DOCBASE_TEAM')
ARTICLE_ID = '707448'  # 指定された記事ID

# ヘッダーの設定
headers = {
    'X-DocBaseToken': API_TOKEN,
    'Content-Type': 'application/json'
}

def get_article_history():
    """記事の履歴を取得"""
    url = f'https://api.docbase.io/teams/{TEAM}/posts/{ARTICLE_ID}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        article_data = response.json()
        
        # 現在の内容を保存
        with open('current_article.json', 'w', encoding='utf-8') as f:
            json.dump(article_data, f, ensure_ascii=False, indent=2)
        
        print(f"記事タイトル: {article_data.get('title', 'タイトルなし')}")
        print(f"最終更新日時: {article_data.get('updated_at', '不明')}")
        print(f"作成日時: {article_data.get('created_at', '不明')}")
        print(f"更新者: {article_data.get('user', {}).get('name', '不明')}")
        print("\n現在の記事データを current_article.json に保存しました。")
        
        # 記事の本文も別ファイルに保存
        with open('current_article_body.md', 'w', encoding='utf-8') as f:
            f.write(article_data.get('body', ''))
        print("記事本文を current_article_body.md に保存しました。")
        
        return article_data
        
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
        return None

if __name__ == "__main__":
    if not API_TOKEN or not TEAM:
        print("環境変数 DOCBASE_API_TOKEN と DOCBASE_TEAM を設定してください。")
    else:
        get_article_history()