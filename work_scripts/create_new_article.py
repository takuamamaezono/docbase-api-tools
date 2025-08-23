#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Docbase新規記事作成スクリプト
既存のdocbase_helper.pyベースで新規記事作成機能を実装
"""

import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

# .envファイルから環境変数を読み込み
load_dotenv()

def create_article(title, body_file, tags=None):
    """新規記事を作成"""
    
    api_token = os.getenv('DOCBASE_ACCESS_TOKEN') or os.getenv('DOCBASE_API_TOKEN')
    team = os.getenv('DOCBASE_TEAM', 'go')
    
    if not api_token:
        print("❌ エラー: DOCBASE_ACCESS_TOKENが設定されていません")
        return False
    
    headers = {
        'X-DocBaseToken': api_token,
        'Content-Type': 'application/json'
    }
    
    # 記事本文を読み込み
    try:
        with open(body_file, 'r', encoding='utf-8') as f:
            body = f.read()
    except FileNotFoundError:
        print(f"❌ ファイルが見つかりません: {body_file}")
        return False
    
    # 記事データ
    data = {
        'title': title,
        'body': body,
        'draft': False,
        'scope': 'private',  # 従業員のみ（重要）
        'tags': tags or []
    }
    
    # API呼び出し
    url = f"https://api.docbase.io/teams/{team}/posts"
    
    print(f"📝 記事を作成中: {title}")
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        result = response.json()
        article_id = result.get('id')
        article_url = result.get('url')
        
        print(f"✅ 記事が作成されました！")
        print(f"📄 記事ID: {article_id}")
        print(f"🔗 URL: {article_url}")
        
        # 結果をファイルに保存
        result_file = f"article_created_{article_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"📁 詳細情報: {result_file}")
        return result
        
    else:
        print(f"❌ エラー {response.status_code}: {response.text}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("使い方: python create_new_article.py <タイトル> <本文ファイル> [タグ1,タグ2,...]")
        print("例: python create_new_article.py 'Illustrator Plugin Guide' illustrator_search_plugin_guide.md Hammerspoon,Adobe")
        sys.exit(1)
    
    title = sys.argv[1]
    body_file = sys.argv[2]
    tags = sys.argv[3].split(',') if len(sys.argv) > 3 else None
    
    result = create_article(title, body_file, tags)
    
    if result:
        print("\n🎉 記事作成完了！")
    else:
        print("\n❌ 記事作成に失敗しました")