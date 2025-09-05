#!/usr/bin/env python3
"""
DocBase記事1276088を更新するスクリプト
"""

import requests
import os
import json
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 設定
TEAM_NAME = "go"
POST_ID = 1276088
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("エラー: DOCBASE_ACCESS_TOKEN が設定されていません")
    exit(1)

# フォーマット済みの内容を読み込む
print("フォーマット済みの内容を読み込んでいます...")
with open('/Users/g.ohorudingusu/Docbase/formatted_post_content_1276088.md', 'r', encoding='utf-8') as f:
    new_body = f.read()

# 現在の記事情報を読み込んでグループIDを取得
with open('/Users/g.ohorudingusu/Docbase/article_1276088_backup.json', 'r', encoding='utf-8') as f:
    current_article = json.load(f)

# グループIDを取得
group_ids = [group['id'] for group in current_article.get('groups', [])]

# 更新を実行
url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{POST_ID}"
headers = {
    "X-DocBaseToken": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

update_data = {
    "body": new_body,
    "scope": "group",  # ルールに従って従業員のみ（グループ）に設定
    "groups": group_ids  # 現在のグループを維持
}

print(f"記事ID {POST_ID} を更新しています...")
print("PowerArQ FP600セクションを追加中...")

try:
    response = requests.patch(url, headers=headers, json=update_data)
    response.raise_for_status()
    print("✅ 記事の更新に成功しました！")
    print(f"更新日時: {response.json().get('updated_at', 'N/A')}")
    print(f"URL: https://go.docbase.io/posts/{POST_ID}")
    print("\n追加内容：")
    print("- PowerArQ FP600セクションを追加")
    print("- バリエーション: コヨーテタン")
    print("- SKU: A0055")
    print("- 販売状況: 空欄")
except requests.exceptions.RequestException as e:
    print(f"❌ 記事の更新に失敗しました: {e}")
    if hasattr(e, 'response') and hasattr(e.response, 'text'):
        print(f"エラー詳細: {e.response.text}")