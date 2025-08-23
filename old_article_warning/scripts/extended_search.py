#!/usr/bin/env python3
"""
拡張検索：より多くのページと異なる検索条件で古い記事を探す
"""

import requests
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# 設定
TEAM_NAME = os.getenv("DOCBASE_TEAM", "go")
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

def search_wide_range():
    """
    幅広いページ範囲で検索
    """
    url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts"
    headers = {
        "X-DocBaseToken": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    print("🔍 拡張範囲検索開始")
    print("=" * 40)
    
    # より広い範囲のページを検索
    search_pages = list(range(100, 50, -5))  # 100, 95, 90, ..., 55
    search_pages.extend(list(range(200, 150, -10)))  # 200, 190, 180, ..., 160
    
    all_old_articles = []
    total_articles_checked = 0
    
    for page in search_pages:
        params = {
            "page": page,
            "per_page": 50
        }
        
        try:
            print(f"📖 ページ {page} 検索中...", end="")
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            articles = data.get("posts", [])
            
            if not articles:
                print(" 記事なし")
                continue
            
            print(f" {len(articles)} 件取得")
            total_articles_checked += len(articles)
            
            # 6ヶ月以上古い記事も含めて検索（条件を緩和）
            threshold_6months = datetime.now() - timedelta(days=183)  # 6ヶ月
            threshold_1year = datetime.now() - timedelta(days=365)    # 1年
            
            old_6months = []
            old_1year = []
            
            for article in articles:
                try:
                    updated_at_str = article.get("updated_at") or article.get("created_at")
                    if not updated_at_str:
                        continue
                    
                    updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
                    updated_at_naive = updated_at.replace(tzinfo=None)
                    
                    days_ago = (datetime.now() - updated_at_naive).days
                    
                    article_info = {
                        "id": article.get("id"),
                        "title": article.get("title", "無題"),
                        "updated_at": updated_at_str,
                        "days_ago": days_ago,
                        "url": article.get("url"),
                        "scope": article.get("scope", "unknown")
                    }
                    
                    if updated_at_naive < threshold_1year:
                        old_1year.append(article_info)
                        all_old_articles.append(article_info)
                        
                        years = days_ago // 365
                        months = (days_ago % 365) // 30
                        print(f"   🔴 1年以上前: ID:{article_info['id']} ({years}年{months}ヶ月前)")
                        print(f"      {article_info['title'][:50]}...")
                        
                    elif updated_at_naive < threshold_6months:
                        old_6months.append(article_info)
                        months = days_ago // 30
                        print(f"   🟡 6ヶ月以上前: ID:{article_info['id']} ({months}ヶ月前)")
                        print(f"      {article_info['title'][:40]}...")
                        
                except Exception as e:
                    continue
            
            if old_1year:
                print(f"   ✅ 1年以上前の記事: {len(old_1year)} 件")
            if old_6months:
                print(f"   ⚠️  6ヶ月以上前の記事: {len(old_6months)} 件")
            
            # 1年以上古い記事が見つかったら一定数で停止
            if len(all_old_articles) >= 20:
                print(f"\n🎯 {len(all_old_articles)} 件の1年以上古い記事を発見したため検索終了")
                break
                
        except requests.exceptions.RequestException as e:
            print(f" ❌ エラー: {e}")
            continue
    
    print(f"\n📊 検索結果:")
    print(f"   チェックした記事数: {total_articles_checked} 件")
    print(f"   1年以上古い記事: {len(all_old_articles)} 件")
    
    return all_old_articles

def check_specific_old_articles():
    """
    特定の古そうな記事IDを直接チェック
    """
    print(f"\n🔍 特定記事の年数チェック")
    print("-" * 30)
    
    # IDが小さい記事（古い可能性が高い）をチェック
    test_ids = [100000, 200000, 300000, 500000, 700000, 800000, 1000000]
    
    url_base = f"https://api.docbase.io/teams/{TEAM_NAME}/posts"
    headers = {
        "X-DocBaseToken": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    found_old = []
    
    for article_id in test_ids:
        try:
            url = f"{url_base}/{article_id}"
            response = requests.get(url, headers=headers)
            
            if response.status_code == 404:
                print(f"ID:{article_id} - 記事なし")
                continue
                
            response.raise_for_status()
            article = response.json()
            
            updated_at_str = article.get("updated_at") or article.get("created_at")
            if not updated_at_str:
                continue
            
            updated_at = datetime.fromisoformat(updated_at_str.replace('Z', '+00:00'))
            updated_at_naive = updated_at.replace(tzinfo=None)
            days_ago = (datetime.now() - updated_at_naive).days
            years = days_ago // 365
            
            print(f"ID:{article_id} - {years}年前 - {article.get('title', '無題')[:30]}...")
            
            if days_ago >= 365:
                found_old.append({
                    "id": article_id,
                    "title": article.get("title", "無題"),
                    "updated_at": updated_at_str,
                    "days_ago": days_ago,
                    "url": article.get("url"),
                    "scope": article.get("scope", "unknown")
                })
                
        except requests.exceptions.RequestException as e:
            print(f"ID:{article_id} - エラー: {e}")
            continue
    
    return found_old

def main():
    print("🚀 拡張古い記事検索システム")
    print("=" * 50)
    
    # 1. 広範囲ページ検索
    old_articles_wide = search_wide_range()
    
    # 2. 特定ID検索
    old_articles_specific = check_specific_old_articles()
    
    # 結果をまとめる
    all_found = old_articles_wide + old_articles_specific
    
    # 重複を除去
    unique_articles = {}
    for article in all_found:
        unique_articles[article["id"]] = article
    
    final_old_articles = list(unique_articles.values())
    
    print(f"\n🎉 最終結果:")
    print(f"   発見した1年以上古い記事: {len(final_old_articles)} 件")
    
    if final_old_articles:
        # 結果を保存
        filename = "extended_old_articles.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_old_articles, f, ensure_ascii=False, indent=2)
        
        print(f"💾 {filename} に保存しました")
        
        # サンプル表示
        print(f"\n📋 発見した古い記事（サンプル）:")
        for i, article in enumerate(sorted(final_old_articles, key=lambda x: x["days_ago"], reverse=True)[:5], 1):
            years = article["days_ago"] // 365
            months = (article["days_ago"] % 365) // 30
            print(f"   {i}. ID:{article['id']} ({years}年{months}ヶ月前)")
            print(f"      {article['title'][:50]}...")
        
        print(f"\n🎯 次のステップ:")
        print(f"   python add_old_article_warning.py --test")
        
    else:
        print(f"\n💡 拡張検索でも1年以上古い記事は見つかりませんでした")
        print("   このDocbaseは非常に活発に更新されているようです！")

if __name__ == "__main__":
    main()