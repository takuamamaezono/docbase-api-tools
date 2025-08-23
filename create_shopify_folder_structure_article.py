#!/usr/bin/env python3
"""
Shopifyフォルダ構成記事をDocbaseに投稿するスクリプト
"""
import requests
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# .envファイルから設定を読み込む
TEAM_NAME = os.getenv("DOCBASE_TEAM", "go")
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

# 記事のタイトル
ARTICLE_TITLE = "🛍️ PowerArQ Shopify開発環境 - フォルダ構成完全ガイド"

# 記事の本文を読み込み
with open('docbase_folder_structure_article.md', 'r', encoding='utf-8') as f:
    ARTICLE_BODY = f.read()

# タグ設定
TAGS = [
    "Shopify",
    "フォルダ構成", 
    "開発環境",
    "PowerArQ",
    "作業ガイド",
    "GitHub管理"
]

def create_docbase_article():
    """記事を作成する"""
    
    if not ACCESS_TOKEN:
        print("❌ ACCESS_TOKEN が設定されていません。.envファイルを確認してください。")
        return None
    
    # APIのURL
    url = f"https://{TEAM_NAME}.docbase.io/api/v1/posts"
    
    # ヘッダー
    headers = {
        "X-DocBaseToken": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    # リクエストボディ
    data = {
        "title": ARTICLE_TITLE,
        "body": ARTICLE_BODY,
        "draft": False,
        "scope": "everyone",
        "tags": TAGS
    }
    
    try:
        print(f"🚀 Docbase記事を作成中...")
        print(f"チーム: {TEAM_NAME}")
        print(f"タイトル: {ARTICLE_TITLE}")
        print(f"タグ: {', '.join(TAGS)}")
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            result = response.json()
            print(f"\n✅ Docbase記事の作成に成功しました！")
            print(f"📄 記事ID: {result['id']}")
            print(f"🔗 記事URL: {result['url']}")
            print(f"📝 タイトル: {result['title']}")
            print(f"🏷️  タグ: {', '.join(result.get('tags', []))}")
            return result
            
        else:
            print(f"\n❌ 記事作成に失敗しました")
            print(f"ステータスコード: {response.status_code}")
            print(f"エラー詳細: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        return None

if __name__ == "__main__":
    result = create_docbase_article()
    if result:
        print(f"\n🎉 完了！記事が正常に作成されました。")
        print(f"👀 記事を確認: {result['url']}")
    else:
        print(f"\n💥 記事作成に失敗しました。")