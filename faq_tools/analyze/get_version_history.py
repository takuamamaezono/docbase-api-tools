#!/usr/bin/env python3
"""
Docbase記事の編集履歴を取得するスクリプト
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def get_article_versions(team_name, access_token, post_id):
    """記事の編集履歴を取得"""
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    # 記事の編集履歴を取得
    url = f"{base_url}/teams/{team_name}/posts/{post_id}/versions"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"編集履歴の取得に失敗しました: {e}")
        return None

def get_specific_version(team_name, access_token, post_id, version_id):
    """特定のバージョンの記事内容を取得"""
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/teams/{team_name}/posts/{post_id}/versions/{version_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"バージョン {version_id} の取得に失敗しました: {e}")
        return None

def format_datetime(datetime_str):
    """日時文字列をフォーマット"""
    try:
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return dt.strftime('%Y年%m月%d日 %H:%M:%S')
    except:
        return datetime_str

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("📜 Docbase記事の編集履歴を取得中...")
    print("=" * 60)
    
    # 編集履歴を取得
    versions = get_article_versions(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not versions:
        print("❌ 編集履歴の取得に失敗しました")
        return
    
    print(f"📊 編集履歴: {len(versions)} 件")
    print()
    
    # 7月22日前後の編集履歴を特定
    target_versions = []
    
    for i, version in enumerate(versions):
        created_at = version.get('created_at', '')
        updated_by = version.get('user', {}).get('name', 'Unknown')
        version_id = version.get('id')
        
        print(f"{i+1:2d}. バージョンID: {version_id}")
        print(f"    更新日時: {format_datetime(created_at)}")
        print(f"    更新者: {updated_by}")
        print()
        
        # 7月21日〜23日の更新を特定
        if '2025-07' in created_at:
            day = created_at.split('T')[0].split('-')[2]
            if day in ['21', '22', '23']:
                target_versions.append({
                    'version_id': version_id,
                    'date': created_at,
                    'user': updated_by,
                    'day': day
                })
    
    if not target_versions:
        print("🔍 7月21日〜23日の編集履歴が見つかりません")
        # 最新の数件を対象版として表示
        print("最新の編集履歴から確認:")
        for version in versions[:5]:
            target_versions.append({
                'version_id': version.get('id'),
                'date': version.get('created_at', ''),
                'user': version.get('user', {}).get('name', 'Unknown'),
                'day': 'recent'
            })
    
    print("=" * 60)
    print("🎯 対象期間の編集履歴:")
    
    for version_info in target_versions:
        print(f"📝 {version_info['day']}日 - {format_datetime(version_info['date'])}")
        print(f"   更新者: {version_info['user']}")
        print(f"   バージョンID: {version_info['version_id']}")
        print()
    
    # 7月22日更新前の版（7月21日の最終版）を特定
    pre_update_version = None
    post_update_version = None
    
    for version_info in sorted(target_versions, key=lambda x: x['date']):
        if version_info['day'] == '21' or (version_info['day'] == '22' and 'Claude' not in version_info['user']):
            pre_update_version = version_info['version_id']
        elif version_info['day'] == '22' and 'Claude' in version_info['user']:
            post_update_version = version_info['version_id']
            break
    
    if pre_update_version:
        print(f"🔍 7月22日更新前の版を取得中... (バージョンID: {pre_update_version})")
        
        pre_version_data = get_specific_version(TEAM_NAME, ACCESS_TOKEN, POST_ID, pre_update_version)
        
        if pre_version_data:
            # 7月22日更新前の内容をファイルに保存
            with open('article_pre_update.json', 'w', encoding='utf-8') as f:
                json.dump(pre_version_data, f, ensure_ascii=False, indent=2)
            
            print("✅ 7月22日更新前の記事内容を article_pre_update.json に保存しました")
            
            # 簡単な統計情報
            body = pre_version_data.get('body', '')
            question_count = body.count('#### Q:')
            
            print(f"📊 7月22日更新前の統計:")
            print(f"   - 記事の文字数: {len(body):,} 文字")
            print(f"   - 質問数: {question_count} 個")
            
        else:
            print("❌ 7月22日更新前の版の取得に失敗しました")
    else:
        print("⚠️ 7月22日更新前の版が特定できませんでした")
    
    print()
    print("💡 次のステップ:")
    print("   1. article_pre_update.json と現在の記事を比較")
    print("   2. 削除された質問を特定")
    print("   3. 必要に応じて復元")

if __name__ == "__main__":
    main()