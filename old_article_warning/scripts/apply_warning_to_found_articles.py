#!/usr/bin/env python3
"""
発見された古い記事に注意書きを追加するスクリプト
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

def load_found_articles(filename="extended_old_articles.json"):
    """
    発見された古い記事のリストを読み込み
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        print(f"📚 {filename} から {len(articles)} 件の古い記事を読み込みました")
        return articles
    except FileNotFoundError:
        print(f"❌ ファイル '{filename}' が見つかりません")
        print("まず extended_search.py を実行してください")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSONファイルの読み込みエラー: {e}")
        return []

def get_article_content(article_id):
    """
    記事の詳細内容を取得
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
        print(f"   ❌ 記事取得エラー: {e}")
        return None

def has_warning_already(body):
    """
    既に注意書きが存在するかチェック
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

def add_warning_to_article(article_info, dry_run=True):
    """
    記事に注意書きを追加
    """
    article_id = article_info["id"]
    title = article_info["title"][:50]
    years = article_info["days_ago"] // 365
    months = (article_info["days_ago"] % 365) // 30
    
    print(f"📖 ID:{article_id} ({years}年{months}ヶ月前) - {title}...")
    
    # 記事内容を取得
    article = get_article_content(article_id)
    if not article:
        return False
    
    body = article.get("body", "")
    
    # 既に注意書きがあるかチェック
    if has_warning_already(body):
        print(f"   ⏭️  既に注意書き済み")
        return True
    
    # 新しい本文を作成
    new_body = WARNING_TEXT + body
    
    if dry_run:
        print(f"   ✏️  注意書きを追加予定（dry_run モード）")
        return True
    
    # 実際に記事を更新
    url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{article_id}"
    headers = {
        "X-DocBaseToken": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    update_data = {"body": new_body}
    
    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        print(f"   ✅ 注意書き追加完了")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 更新エラー: {e}")
        return False

def process_found_articles(dry_run=True, max_articles=None):
    """
    発見された古い記事を処理
    """
    print("🚀 発見された古い記事への注意書き追加")
    print("=" * 60)
    
    # 古い記事リストを読み込み
    old_articles = load_found_articles()
    
    if not old_articles:
        return
    
    # 最も古い順にソート
    old_articles.sort(key=lambda x: x["days_ago"], reverse=True)
    
    if dry_run:
        print("🔍 DRY RUN モード: 実際の更新は行いません")
    else:
        print("⚠️  実際に記事を更新します")
        print("🔥 --execute モードで実行中...")
    
    # 処理件数を制限（テスト用）
    if max_articles:
        old_articles = old_articles[:max_articles]
        print(f"📊 テスト用に最初の {max_articles} 件のみ処理します")
    
    print(f"\n🔧 {len(old_articles)} 件の記事を処理開始")
    print("-" * 60)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, article in enumerate(old_articles, 1):
        print(f"[{i:3d}/{len(old_articles)}]", end=" ")
        
        if add_warning_to_article(article, dry_run=dry_run):
            success_count += 1
        else:
            error_count += 1
        
        # API制限対策
        if not dry_run:
            time.sleep(2)  # 2秒待機
        else:
            time.sleep(0.1)  # dry_runは短い待機
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 処理完了サマリー:")
    print(f"   処理対象: {len(old_articles)} 件")
    print(f"   成功: {success_count} 件")
    print(f"   エラー: {error_count} 件")
    
    if dry_run:
        print(f"\n🎯 実際に更新する場合:")
        print(f"   python apply_warning_to_found_articles.py --execute")
        
        # 最も古い記事を表示
        if old_articles:
            oldest = old_articles[0]  # 既にソート済み
            years = oldest["days_ago"] // 365
            months = (oldest["days_ago"] % 365) // 30
            print(f"\n🏆 最も古い記事:")
            print(f"   ID: {oldest['id']}")
            print(f"   タイトル: {oldest['title'][:50]}...")
            print(f"   更新日: {oldest['updated_at']}")
            print(f"   経過: {years}年{months}ヶ月前")

def main():
    import sys
    
    # コマンドライン引数の処理
    dry_run = True
    max_articles = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--execute":
            dry_run = False
        elif sys.argv[1] == "--test":
            max_articles = 5  # テスト用に5件のみ
    
    print("💡 使用方法:")
    print("   python apply_warning_to_found_articles.py           # 確認のみ（推奨）")
    print("   python apply_warning_to_found_articles.py --test    # 5件のみテスト")
    print("   python apply_warning_to_found_articles.py --execute # 実際に更新")
    print()
    
    # メイン処理を実行
    process_found_articles(dry_run=dry_run, max_articles=max_articles)

if __name__ == "__main__":
    main()