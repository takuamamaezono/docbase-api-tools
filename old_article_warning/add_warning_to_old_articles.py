#!/usr/bin/env python3
"""
1年以上更新されていない記事に注意書きを一括追加するメインスクリプト
"""

import requests
import os
import json
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

def get_all_articles_paginated(max_pages=50):
    """
    全記事を段階的に取得（大量記事対応）
    """
    url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts"
    headers = {
        "X-DocBaseToken": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    all_articles = []
    page = 1
    per_page = 50  # 効率化のため50件ずつ
    
    print(f"📚 全記事を取得中（最大 {max_pages * per_page} 件）...")
    
    while page <= max_pages:
        params = {
            "page": page,
            "per_page": per_page
        }
        
        try:
            print(f"   ページ {page} 取得中...", end="")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get("posts", [])
            
            if not articles:
                print(" 記事なし（終了）")
                break
                
            all_articles.extend(articles)
            print(f" {len(articles)} 件取得（累計: {len(all_articles)} 件）")
            
            page += 1
            time.sleep(0.5)  # API制限対策
            
        except requests.exceptions.RequestException as e:
            print(f" ❌ エラー: {e}")
            break
    
    print(f"✅ 合計 {len(all_articles)} 件の記事を取得完了")
    return all_articles

def find_articles_needing_warning(articles, months_threshold=12):
    """
    注意書きが必要な記事を特定
    """
    threshold_date = datetime.now() - timedelta(days=months_threshold * 30)
    target_articles = []
    
    print(f"\n🔍 {months_threshold}ヶ月以上更新されていない記事を検索...")
    print(f"基準日: {threshold_date.strftime('%Y-%m-%d')}")
    
    for article in articles:
        try:
            updated_at_str = article.get("updated_at") or article.get("created_at")
            if not updated_at_str:
                continue
            
            # 日時をパース
            updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
            updated_at_naive = updated_at.replace(tzinfo=None)
            
            if updated_at_naive < threshold_date:
                article_info = {
                    "id": article.get("id"),
                    "title": article.get("title", "無題"),
                    "updated_at": updated_at_str,
                    "url": article.get("url"),
                    "scope": article.get("scope", "unknown")
                }
                target_articles.append(article_info)
                
        except Exception as e:
            continue
    
    print(f"📊 対象記事: {len(target_articles)} 件")
    return target_articles

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
        print(f"❌ 記事取得エラー (ID: {article_id}): {e}")
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

def add_warning_to_article(article_id, dry_run=True):
    """
    記事に注意書きを追加
    """
    # 記事内容を取得
    article = get_article_content(article_id)
    if not article:
        return False
    
    title = article.get("title", "無題")
    body = article.get("body", "")
    
    # 既に注意書きがあるかチェック
    if has_warning_already(body):
        print(f"   ⏭️  既に注意書き済み")
        return True
    
    # 新しい本文を作成
    new_body = WARNING_TEXT + body
    
    if dry_run:
        print(f"   ✏️  注意書き追加予定（dry_run）")
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

def process_all_old_articles(dry_run=True, max_articles=None):
    """
    古い記事を一括処理するメイン関数
    """
    print("🚀 古い記事への注意書き一括追加システム")
    print("=" * 60)
    
    if dry_run:
        print("🔍 DRY RUN モード: 実際の更新は行いません")
    else:
        print("⚠️  実際に記事を更新します")
        input("続行するには Enter を押してください...")
    
    # 全記事を取得
    all_articles = get_all_articles_paginated(max_pages=50)
    
    if not all_articles:
        print("❌ 記事が取得できませんでした")
        return
    
    # 古い記事を特定
    old_articles = find_articles_needing_warning(all_articles)
    
    if not old_articles:
        print("🎉 1年以上古い記事は見つかりませんでした！")
        print("   すべての記事が最新の状態です。")
        return
    
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
        article_id = article.get("id")
        title = article.get("title", "無題")[:50]
        
        print(f"[{i:3d}/{len(old_articles)}] ID:{article_id} - {title}...")
        
        if add_warning_to_article(article_id, dry_run=dry_run):
            success_count += 1
        else:
            error_count += 1
        
        # API制限対策
        if not dry_run:
            time.sleep(2)  # 2秒待機
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("📊 処理完了サマリー:")
    print(f"   処理対象: {len(old_articles)} 件")
    print(f"   成功: {success_count} 件")
    print(f"   エラー: {error_count} 件")
    
    if dry_run:
        print(f"\n🎯 実際に更新する場合:")
        print(f"   python add_warning_to_old_articles.py --execute")

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
    print("   python add_warning_to_old_articles.py           # 確認のみ（推奨）")
    print("   python add_warning_to_old_articles.py --test    # 5件のみテスト")
    print("   python add_warning_to_old_articles.py --execute # 実際に更新")
    print()
    
    # メイン処理を実行
    process_all_old_articles(dry_run=dry_run, max_articles=max_articles)

if __name__ == "__main__":
    main()