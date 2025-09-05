#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# 環境変数を取得
ACCESS_TOKEN = os.getenv('DOCBASE_ACCESS_TOKEN')
TEAM = os.getenv('DOCBASE_TEAM')

def read_markdown_file(file_path):
    """マークダウンファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"ファイル読み込みエラー: {e}")
        return None

def create_docbase_post(title, body, tags=None):
    """Docbaseに新しい記事を作成"""
    
    # APIエンドポイント
    url = f'https://api.docbase.io/teams/{TEAM}/posts'
    
    # ヘッダー設定
    headers = {
        'X-DocBaseToken': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    
    # リクエストボディ
    data = {
        'title': title,
        'body': body,
        'draft': False,  # 下書きではなく公開
        'tags': tags or ['営業部', '組織紹介']
    }
    
    try:
        # APIリクエスト実行
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ 記事が正常に作成されました！")
            print(f"📝 記事タイトル: {result['title']}")
            print(f"🔗 記事URL: {result['url']}")
            print(f"📅 作成日時: {result['created_at']}")
            return result
        else:
            print(f"❌ 記事作成に失敗しました。")
            print(f"ステータスコード: {response.status_code}")
            print(f"エラー内容: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ APIリクエストでエラーが発生しました: {e}")
        return None

def main():
    print("🚀 営業先着事業部紹介記事をDocbaseにアップロード中...")
    
    # マークダウンファイルを読み込み
    markdown_file = '/Users/g.ohorudingusu/Docbase/営業先着事業部紹介記事.md'
    body_content = read_markdown_file(markdown_file)
    
    if not body_content:
        print("❌ マークダウンファイルの読み込みに失敗しました。")
        return
    
    # 記事を作成
    title = "🏢 営業先着事業部のご紹介"
    tags = ['営業部', '組織紹介', '事業部紹介', 'メンバー', 'PowerArQ']
    
    result = create_docbase_post(title, body_content, tags)
    
    if result:
        print("\n🎉 アップロード完了！")
        print(f"記事ID: {result['id']}")
    else:
        print("\n💥 アップロードに失敗しました。")

if __name__ == "__main__":
    main()