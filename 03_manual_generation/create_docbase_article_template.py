#!/usr/bin/env python3
"""
Docbase記事作成のテンプレートスクリプト
すべての記事は従業員のみ（G.O / 加島）の公開範囲で作成されます
"""

import requests
import os
import sys
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# 設定
TEAM_NAME = os.getenv("DOCBASE_TEAM", "go")
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("エラー: DOCBASE_ACCESS_TOKEN が設定されていません")
    exit(1)

def create_docbase_article(title, body, tags=None):
    """
    Docbase記事を作成する（統一設定：従業員のみ公開）
    
    Args:
        title: 記事タイトル
        body: 記事本文（Markdown）
        tags: タグのリスト（省略可）
    
    Returns:
        作成された記事の情報（辞書形式）
    """
    if tags is None:
        tags = []
    
    # 記事作成データ（統一設定）
    article_data = {
        "title": title,
        "body": body,
        "draft": False,
        "scope": "private",  # 従業員のみ（G.O / 加島）- 統一設定
        "tags": tags
    }
    
    # Docbase APIに記事を作成
    url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts"
    headers = {
        "X-DocBaseToken": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    print(f"Docbaseに記事を作成中...")
    print(f"タイトル: {title}")
    print(f"公開範囲: 従業員のみ（G.O / 加島）")
    print(f"タグ: {', '.join(tags) if tags else 'なし'}")
    print("-" * 50)
    
    try:
        response = requests.post(url, headers=headers, json=article_data)
        response.raise_for_status()
        
        result = response.json()
        print("✅ 記事の作成に成功しました！")
        print(f"記事ID: {result.get('id')}")
        print(f"記事タイトル: {result.get('title')}")
        print(f"公開範囲: {result.get('scope')} (従業員のみ)")
        print(f"URL: {result.get('url')}")
        print(f"作成日時: {result.get('created_at')}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 記事の作成に失敗しました: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"ステータスコード: {e.response.status_code}")
            print(f"エラー詳細: {e.response.text}")
        return None

def main():
    """
    使用例として、コマンドライン引数から記事を作成
    """
    if len(sys.argv) < 3:
        print("使用方法: python create_docbase_article_template.py <タイトル> <本文ファイルパス> [タグ1,タグ2,...]")
        print("")
        print("例:")
        print("  python create_docbase_article_template.py '新機能マニュアル' './manual.md' 'システム,マニュアル'")
        exit(1)
    
    title = sys.argv[1]
    body_file_path = sys.argv[2]
    tags = sys.argv[3].split(',') if len(sys.argv) > 3 else []
    
    # 本文ファイルを読み込み
    try:
        with open(body_file_path, 'r', encoding='utf-8') as f:
            body = f.read()
    except FileNotFoundError:
        print(f"エラー: ファイル '{body_file_path}' が見つかりません")
        exit(1)
    except Exception as e:
        print(f"エラー: ファイル読み込みに失敗しました: {e}")
        exit(1)
    
    # 記事を作成
    result = create_docbase_article(title, body, tags)
    
    if result:
        print(f"\n🎉 記事作成完了！")
        print(f"従業員のみの公開範囲で作成されました。")
    else:
        print(f"\n❌ 記事作成に失敗しました。")

if __name__ == "__main__":
    main()