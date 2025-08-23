#!/usr/bin/env python3
"""
Asana-Docbase拡張機能のマニュアル記事を新規作成するスクリプト
"""

import requests
import json
import os

# 設定
TEAM_NAME = "go"
ACCESS_TOKEN = "docbase_25Nx-5dwQuuqMcwz3ycgdEwNTzECPxxuh7Ry5jrbfH6MC5gxYj2uxakyDGeaYP2X"

# マニュアルファイルの内容を読み込む
manual_file_path = "/Users/g.ohorudingusu/asana-docbase-extension/DOCBASE_MANUAL.md"
print(f"マニュアルファイルを読み込んでいます: {manual_file_path}")

try:
    with open(manual_file_path, 'r', encoding='utf-8') as f:
        manual_content = f.read()
    print(f"✅ マニュアル内容を読み込みました ({len(manual_content)}文字)")
except FileNotFoundError:
    print(f"❌ ファイルが見つかりません: {manual_file_path}")
    exit(1)

# 記事作成データ
create_data = {
    "title": "🔗 Asana-Docbase連携拡張機能 マニュアル",
    "body": manual_content,
    "tags": ["Chrome拡張機能", "Asana", "FAQ", "マニュアル", "ツール"],
    "scope": "everyone",  # 全員に公開
    "draft": False  # 公開状態で作成
}

# Docbase API呼び出し
url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts"
headers = {
    "X-DocBaseToken": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

print("Docbase記事を作成しています...")
print(f"タイトル: {create_data['title']}")
print(f"タグ: {', '.join(create_data['tags'])}")

try:
    response = requests.post(url, headers=headers, json=create_data)
    response.raise_for_status()
    
    # 成功時の処理
    result = response.json()
    article_id = result.get('id')
    article_url = result.get('url')
    
    print("🎉 記事の作成に成功しました！")
    print(f"記事ID: {article_id}")
    print(f"記事URL: {article_url}")
    print(f"作成日時: {result.get('created_at', 'N/A')}")
    print(f"公開URL: https://go.docbase.io/posts/{article_id}")
    
    # 結果をファイルに保存
    result_data = {
        "article_id": article_id,
        "article_url": article_url,
        "title": create_data["title"],
        "created_at": result.get('created_at'),
        "tags": create_data["tags"]
    }
    
    with open('/Users/g.ohorudingusu/Docbase/asana_manual_creation_result.json', 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print("📝 作成結果を asana_manual_creation_result.json に保存しました")
    
except requests.exceptions.RequestException as e:
    print(f"❌ 記事の作成に失敗しました: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print(f"ステータスコード: {e.response.status_code}")
        print(f"エラー詳細: {e.response.text}")