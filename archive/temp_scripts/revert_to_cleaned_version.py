#!/usr/bin/env python3
import os
import json
import requests
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数の設定
API_TOKEN = os.getenv('DOCBASE_ACCESS_TOKEN')
TEAM = os.getenv('DOCBASE_TEAM')
ARTICLE_ID = '707448'

# ヘッダーの設定
headers = {
    'X-DocBaseToken': API_TOKEN,
    'Content-Type': 'application/json'
}

def revert_article():
    """削除したFAQを含まない状態に戻す"""
    print("12:28更新の記事内容を読み込み中...")
    
    # 12:28に更新されたクリーンな記事を読み込む
    # この時点の記事は /Users/g.ohorudingusu/Docbase/current_article_body.md に保存されている
    with open('current_article_body.md', 'r', encoding='utf-8') as f:
        cleaned_body = f.read()
    
    # 現在の記事データを取得（グループ情報等のため）
    with open('current_article.json', 'r', encoding='utf-8') as f:
        current_data = json.load(f)
    
    current_title = current_data.get('title', '')
    current_groups = current_data.get('groups', [])
    
    print(f"記事タイトル: {current_title}")
    print(f"クリーンな本文長: {len(cleaned_body)} 文字")
    
    # グループIDのリストを作成
    group_ids = [group['id'] for group in current_groups]
    
    # 更新用のデータを準備
    update_data = {
        'title': current_title,
        'body': cleaned_body,
        'notice': True,
        'scope': current_data.get('scope', 'group'),
        'groups': group_ids
    }
    
    # 記事を更新
    url = f'https://api.docbase.io/teams/{TEAM}/posts/{ARTICLE_ID}'
    
    print(f"\n記事をクリーンな状態に戻しています...")
    
    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ 記事を元の状態（削除済みFAQを含まない）に戻しました！")
        print(f"更新日時: {result.get('updated_at')}")
        print(f"記事URL: {result.get('url')}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ エラーが発生しました: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"ステータスコード: {e.response.status_code}")
            print(f"エラー内容: {e.response.text}")
        return None

if __name__ == "__main__":
    if not API_TOKEN or not TEAM:
        print("環境変数 DOCBASE_ACCESS_TOKEN と DOCBASE_TEAM を設定してください。")
    else:
        revert_article()