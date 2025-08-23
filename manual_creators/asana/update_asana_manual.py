#!/usr/bin/env python3
"""
作成したAsana-Docbase拡張機能マニュアル記事を更新するスクリプト
"""

import requests
import json

# 設定
TEAM_NAME = "go"
ARTICLE_ID = 3873863  # 先ほど作成した記事ID
ACCESS_TOKEN = "docbase_25Nx-5dwQuuqMcwz3ycgdEwNTzECPxxuh7Ry5jrbfH6MC5gxYj2uxakyDGeaYP2X"

# 更新されたマニュアルファイルの内容を読み込む
manual_file_path = "/Users/g.ohorudingusu/asana-docbase-extension/DOCBASE_MANUAL.md"
print(f"更新されたマニュアルファイルを読み込んでいます: {manual_file_path}")

try:
    with open(manual_file_path, 'r', encoding='utf-8') as f:
        updated_content = f.read()
    print(f"✅ 更新内容を読み込みました ({len(updated_content)}文字)")
except FileNotFoundError:
    print(f"❌ ファイルが見つかりません: {manual_file_path}")
    exit(1)

# 記事更新データ
update_data = {
    "body": updated_content
}

# Docbase API呼び出し
url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{ARTICLE_ID}"
headers = {
    "X-DocBaseToken": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

print(f"記事ID {ARTICLE_ID} を更新しています...")

try:
    response = requests.patch(url, headers=headers, json=update_data)
    response.raise_for_status()
    
    # 成功時の処理
    result = response.json()
    
    print("🎉 記事の更新に成功しました！")
    print(f"記事ID: {ARTICLE_ID}")
    print(f"更新日時: {result.get('updated_at', 'N/A')}")
    print(f"記事URL: https://go.docbase.io/posts/{ARTICLE_ID}")
    
except requests.exceptions.RequestException as e:
    print(f"❌ 記事の更新に失敗しました: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"ステータスコード: {e.response.status_code}")
        print(f"エラー詳細: {e.response.text}")