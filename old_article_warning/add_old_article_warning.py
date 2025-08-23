#!/usr/bin/env python3
"""
1年以上更新されていない記事の先頭に注意書きを追加するスクリプト
"""

import requests
import json
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# 設定
TEAM_NAME = os.getenv("DOCBASE_TEAM", "go")
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("エラー: DOCBASE_ACCESS_TOKEN が設定されていません")
    exit(1)

# 注意書きのテンプレート
WARNING_TEXT = """⚠️ **この記事は1年以上前に書かれたものです。情報が古い可能性があります。**

---

"""

def get_article_content(article_id):
    """
    指定された記事の内容を取得する
    
    Args:
        article_id: 記事ID
    
    Returns:
        記事の詳細情報（辞書形式）
    """
    url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{article_id}"
    headers = {
        "X-DocBaseToken": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 記事取得エラー (ID: {article_id}): {e}")
        return None

def has_warning_already(body):
    """
    既に注意書きが追加されているかチェック
    
    Args:
        body: 記事本文
    
    Returns:
        bool: 注意書きが存在する場合True
    """
    warning_indicators = [
        "この記事は1年以上前に書かれたものです",
        "情報が古い可能性があります",
        "⚠️ **この記事は1年以上前"
    ]
    
    for indicator in warning_indicators:
        if indicator in body:
            return True
    return False

def add_warning_to_article(article_id, dry_run=True):
    """
    記事に注意書きを追加する
    
    Args:
        article_id: 記事ID
        dry_run: True の場合、実際の更新は行わず確認のみ
    
    Returns:
        bool: 成功時True
    """
    print(f"📖 記事ID {article_id} を処理中...")
    
    # 記事内容を取得
    article = get_article_content(article_id)
    if not article:
        return False
    
    title = article.get("title", "無題")
    body = article.get("body", "")
    
    print(f"   タイトル: {title}")
    
    # 既に注意書きがあるかチェック
    if has_warning_already(body):
        print(f"   ⏭️  既に注意書きが追加済みです")
        return True
    
    # 新しい本文を作成（注意書きを先頭に追加）
    new_body = WARNING_TEXT + body
    
    if dry_run:
        print(f"   ✏️  注意書きを追加予定（dry_run モード）")
        print(f"   📝 追加する注意書き:")
        print(f"      {WARNING_TEXT.strip()}")
        return True
    
    # 実際に記事を更新
    url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{article_id}"
    headers = {
        "X-DocBaseToken": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    update_data = {
        "body": new_body
    }
    
    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        print(f"   ✅ 注意書きを追加しました")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 更新エラー: {e}")
        return False

def process_articles_from_file(filename="old_articles.json", dry_run=True, max_articles=None):
    """
    JSONファイルから古い記事のリストを読み込んで処理する
    
    Args:
        filename: 古い記事のJSONファイル
        dry_run: True の場合、実際の更新は行わず確認のみ
        max_articles: 処理する最大記事数（テスト用）
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            old_articles = json.load(f)
    except FileNotFoundError:
        print(f"❌ ファイル '{filename}' が見つかりません")
        print("まず find_old_articles.py を実行してください")
        return
    except json.JSONDecodeError as e:
        print(f"❌ JSONファイルの読み込みエラー: {e}")
        return
    
    print(f"📚 {len(old_articles)} 件の古い記事を処理します")
    
    if dry_run:
        print("🔍 DRY RUN モード: 実際の更新は行いません")
    else:
        print("⚠️  実際に記事を更新します")
    
    print("=" * 60)
    
    # 処理する記事数を制限（テスト用）
    if max_articles:
        old_articles = old_articles[:max_articles]
        print(f"📊 テスト用に最初の {max_articles} 件のみ処理します")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, article in enumerate(old_articles, 1):
        article_id = article.get("id")
        if not article_id:
            continue
        
        print(f"\n[{i}/{len(old_articles)}]", end=" ")
        
        # 記事を処理
        if add_warning_to_article(article_id, dry_run=dry_run):
            success_count += 1
        else:
            error_count += 1
        
        # API制限対策（実際の更新時のみ）
        if not dry_run:
            time.sleep(1)  # 1秒待機
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 処理結果サマリー:")
    print(f"   成功: {success_count} 件")
    print(f"   エラー: {error_count} 件")
    print(f"   合計: {len(old_articles)} 件")
    
    if dry_run:
        print("\n🎯 実際に更新する場合は、dry_run=False で実行してください")

def main():
    import sys
    
    # コマンドライン引数の処理
    dry_run = True
    max_articles = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--execute":
            dry_run = False
        elif sys.argv[1] == "--test":
            max_articles = 3  # テスト用に3件のみ
    
    print("🔧 1年以上更新されていない記事への注意書き追加")
    print("=" * 60)
    
    if dry_run and max_articles is None:
        print("💡 使用方法:")
        print("   python add_old_article_warning.py           # 確認のみ（推奨）")
        print("   python add_old_article_warning.py --test    # 3件のみテスト")
        print("   python add_old_article_warning.py --execute # 実際に更新")
        print()
    
    # 記事を処理
    process_articles_from_file(dry_run=dry_run, max_articles=max_articles)

if __name__ == "__main__":
    main()