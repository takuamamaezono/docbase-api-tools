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

def load_json(filename):
    """JSONファイルを読み込む"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def restore_article():
    """削除されたFAQを復元して記事を更新"""
    print("現在の記事とバックアップデータを読み込み中...")
    
    # バックアップから本文を取得
    backup_data = load_json('article_backup.json')
    backup_body = backup_data.get('body', '')
    
    # 現在の記事を取得
    current_data = load_json('current_article.json')
    current_title = current_data.get('title', '')
    current_groups = current_data.get('groups', [])
    
    print(f"記事タイトル: {current_title}")
    print(f"バックアップの本文長: {len(backup_body)} 文字")
    print(f"グループ数: {len(current_groups)}")
    
    # グループIDのリストを作成
    group_ids = [group['id'] for group in current_groups]
    
    # 更新用のデータを準備
    update_data = {
        'title': current_title,
        'body': backup_body,
        'notice': True,
        'scope': current_data.get('scope', 'group'),
        'groups': group_ids
    }
    
    # 記事を更新
    url = f'https://api.docbase.io/teams/{TEAM}/posts/{ARTICLE_ID}'
    
    print(f"\n記事を更新中...")
    print(f"URL: {url}")
    
    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ 記事の更新が完了しました！")
        print(f"更新日時: {result.get('updated_at')}")
        print(f"記事URL: {result.get('url')}")
        
        # 更新後の記事を保存
        with open('restored_article.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ エラーが発生しました: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"ステータスコード: {e.response.status_code}")
            print(f"エラー内容: {e.response.text}")
        return None

def verify_restoration():
    """復元が成功したか確認"""
    print("\n復元結果を確認中...")
    
    # 更新後の記事を取得
    url = f'https://api.docbase.io/teams/{TEAM}/posts/{ARTICLE_ID}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        updated_data = response.json()
        updated_body = updated_data.get('body', '')
        
        # バックアップと比較
        backup_data = load_json('article_backup.json')
        backup_body = backup_data.get('body', '')
        
        if updated_body == backup_body:
            print("✅ 記事の本文が正しく復元されました！")
        else:
            print("⚠️ 記事の本文に差異があります。")
            print(f"更新後の文字数: {len(updated_body)}")
            print(f"バックアップの文字数: {len(backup_body)}")
        
    except requests.exceptions.RequestException as e:
        print(f"確認中にエラーが発生しました: {e}")

if __name__ == "__main__":
    if not API_TOKEN or not TEAM:
        print("環境変数 DOCBASE_ACCESS_TOKEN と DOCBASE_TEAM を設定してください。")
    else:
        result = restore_article()
        if result:
            verify_restoration()