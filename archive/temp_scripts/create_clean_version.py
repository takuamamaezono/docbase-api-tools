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

def create_and_update_clean_version():
    """7/23の削除作業後のクリーンな状態を再現して更新"""
    print("7/23の削除作業後の状態を再現中...")
    
    # 7/23 12:28時点の記事データを取得
    # これは削除される前のFAQが除外された状態
    url = f'https://api.docbase.io/teams/{TEAM}/posts/{ARTICLE_ID}'
    
    try:
        # まず記事の基本情報を取得
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        article_info = response.json()
        
        # 7/23に行われた削除の内容を確認
        # バックアップファイル（削除前）から本文を取得
        with open('article_backup.json', 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        backup_body = backup_data.get('body', '')
        
        # 削除されたFAQリストを読み込む
        with open('deleted_faqs.json', 'r', encoding='utf-8') as f:
            deleted_faqs = json.load(f)
        
        print(f"削除前の本文長: {len(backup_body)} 文字")
        print(f"削除するFAQ数: {len(deleted_faqs)}")
        
        # バックアップから削除されたFAQを除外してクリーンな本文を作成
        cleaned_body = backup_body
        
        # 各削除FAQを本文から取り除く
        removed_count = 0
        for faq in deleted_faqs:
            question = faq['question']
            # FAQセクション全体を探して削除（質問から次の質問まで）
            import re
            
            # パターン: #### Q: 質問 から次の #### Q: または ## セクションまで
            pattern = re.compile(
                rf'#### Q: {re.escape(question)}\n- \[ \] Web反映対象\n.*?(?=#### Q:|## |$)', 
                re.DOTALL
            )
            
            if pattern.search(cleaned_body):
                cleaned_body = pattern.sub('', cleaned_body)
                removed_count += 1
                print(f"削除 {removed_count}/{len(deleted_faqs)}: {question[:50]}...")
        
        # 余分な改行を整理
        cleaned_body = re.sub(r'\n{3,}', '\n\n', cleaned_body)
        
        print(f"\nクリーン後の本文長: {len(cleaned_body)} 文字")
        print(f"実際に削除されたFAQ数: {removed_count}")
        
        # グループ情報を取得
        current_groups = article_info.get('groups', [])
        group_ids = [group['id'] for group in current_groups]
        
        # 更新データを準備
        update_data = {
            'title': article_info.get('title'),
            'body': cleaned_body,
            'notice': True,
            'scope': article_info.get('scope', 'group'),
            'groups': group_ids
        }
        
        # 記事を更新
        print("\n記事を更新中...")
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ 記事を7/23の削除作業後の状態に戻しました！")
        print(f"更新日時: {result.get('updated_at')}")
        print(f"記事URL: {result.get('url')}")
        
        # クリーンな本文を保存
        with open('final_cleaned_body.md', 'w', encoding='utf-8') as f:
            f.write(cleaned_body)
        
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
        create_and_update_clean_version()