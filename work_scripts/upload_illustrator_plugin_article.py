#!/usr/bin/env python3
"""
Illustrator Search Plugin記事をDocbaseにアップロードするスクリプト
"""

import os
import requests
import json
from datetime import datetime

def load_env():
    """環境変数を読み込む"""
    env_path = '/Users/g.ohorudingusu/Docbase/.env'
    env_vars = {}
    
    try:
        with open(env_path, 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
        return env_vars
    except FileNotFoundError:
        print(f"エラー: {env_path} が見つかりません")
        return {}

def create_docbase_article(title, body, tags=None, scope="private"):
    """Docbaseに新しい記事を作成する"""
    
    # 環境変数の読み込み
    env_vars = load_env()
    if not env_vars:
        return False
    
    api_token = env_vars.get('DOCBASE_ACCESS_TOKEN')
    team = env_vars.get('DOCBASE_TEAM')
    
    if not api_token or not team:
        print("エラー: API トークンまたはチーム名が設定されていません")
        return False
    
    # APIエンドポイント
    url = f"https://api.docbase.io/teams/{team}/posts"
    
    # ヘッダー
    headers = {
        'X-DocBase-Token': api_token,
        'Content-Type': 'application/json'
    }
    
    # リクエストボディ
    data = {
        'title': title,
        'body': body,
        'draft': False,
        'scope': scope,  # "private" で従業員のみ
        'tags': tags or []
    }
    
    try:
        print(f"記事をアップロード中: {title}")
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            result = response.json()
            article_id = result.get('id')
            article_url = result.get('url')
            
            print(f"✅ 記事のアップロードが完了しました")
            print(f"📝 記事ID: {article_id}")
            print(f"🔗 記事URL: {article_url}")
            
            return {
                'id': article_id,
                'url': article_url,
                'title': title
            }
        else:
            print(f"❌ エラー: {response.status_code}")
            print(f"レスポンス: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ アップロード中にエラーが発生しました: {str(e)}")
        return False

def main():
    """メイン処理"""
    
    # 記事ファイルの読み込み
    article_file = '/Users/g.ohorudingusu/Docbase/illustrator_search_plugin_guide.md'
    
    try:
        with open(article_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"エラー: {article_file} が見つかりません")
        return
    
    # 記事のタイトルと本文を分離
    lines = content.split('\n')
    title = lines[0].replace('# ', '') if lines and lines[0].startswith('# ') else 'Illustrator Search Plugin ガイド'
    body = content
    
    # タグの設定
    tags = [
        'Hammerspoon',
        'Adobe Illustrator',
        'macOS',
        'プラグイン',
        '効率化ツール',
        'Lua',
        '開発ガイド'
    ]
    
    # 記事をアップロード
    result = create_docbase_article(
        title=title,
        body=body,
        tags=tags,
        scope="private"
    )
    
    if result:
        # 結果をファイルに保存
        result_file = f'/Users/g.ohorudingusu/Docbase/illustrator_plugin_upload_result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"📄 結果詳細: {result_file}")
        print("\n🎉 Illustrator Search Pluginの記事アップロード完了！")
    else:
        print("\n❌ 記事のアップロードに失敗しました")

if __name__ == "__main__":
    main()