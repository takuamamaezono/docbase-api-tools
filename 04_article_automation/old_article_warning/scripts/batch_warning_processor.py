#!/usr/bin/env python3
"""
バッチ処理で古い記事に注意書きを追加（段階実行）
"""

import requests
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

# 設定
TEAM_NAME = os.getenv("DOCBASE_TEAM", "go")
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

# 注意書きのテンプレート
WARNING_TEXT = """⚠️ **この記事は1年以上前に書かれたものです。情報が古い可能性があります。**

---

"""

def process_batch(articles, batch_num, batch_size=10):
    """
    指定されたバッチの記事を処理
    """
    print(f"\n📦 バッチ {batch_num} 処理開始 ({len(articles)} 件)")
    print("-" * 40)
    
    headers = {
        "X-DocBaseToken": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    
    batch_success = 0
    batch_skip = 0
    batch_error = 0
    
    for i, article in enumerate(articles, 1):
        article_id = article["id"]
        title = article["title"][:40]
        years = article["days_ago"] // 365
        months = (article["days_ago"] % 365) // 30
        
        print(f"  [{i:2d}/{len(articles)}] ID:{article_id} ({years}年{months}ヶ月前) - {title}...")
        
        try:
            # 記事を取得
            url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{article_id}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            article_data = response.json()
            body = article_data.get("body", "")
            
            # 既に注意書きがあるかチェック
            if "この記事は1年以上前に書かれたものです" in body:
                print("       ⏭️  既に追加済み")
                batch_skip += 1
                continue
            
            # 注意書きを追加
            new_body = WARNING_TEXT + body
            
            # 記事を更新
            update_data = {"body": new_body}
            update_response = requests.patch(url, headers=headers, json=update_data)
            update_response.raise_for_status()
            
            print("       ✅ 追加完了")
            batch_success += 1
            
            # API制限対策
            time.sleep(1.5)
            
        except requests.exceptions.RequestException as e:
            print(f"       ❌ エラー: {e}")
            batch_error += 1
            continue
    
    print(f"\n📊 バッチ {batch_num} 結果: 成功 {batch_success} / スキップ {batch_skip} / エラー {batch_error}")
    return batch_success, batch_skip, batch_error

def main():
    print("🚀 バッチ処理による古い記事への注意書き追加")
    print("=" * 60)
    
    # 記事リストを読み込み
    try:
        with open('extended_old_articles.json', 'r', encoding='utf-8') as f:
            all_articles = json.load(f)
    except FileNotFoundError:
        print("❌ extended_old_articles.json が見つかりません")
        return
    
    # 最も古い順にソート
    all_articles.sort(key=lambda x: x["days_ago"], reverse=True)
    
    print(f"📚 対象記事: {len(all_articles)} 件")
    print("💡 10件ずつバッチ処理で実行します")
    
    # バッチサイズ
    batch_size = 10
    total_batches = (len(all_articles) + batch_size - 1) // batch_size
    
    total_success = 0
    total_skip = 0
    total_error = 0
    
    # バッチごとに処理
    for batch_num in range(1, total_batches + 1):
        start_idx = (batch_num - 1) * batch_size
        end_idx = min(start_idx + batch_size, len(all_articles))
        batch_articles = all_articles[start_idx:end_idx]
        
        # バッチを処理
        success, skip, error = process_batch(batch_articles, batch_num, batch_size)
        
        total_success += success
        total_skip += skip
        total_error += error
        
        # バッチ間の待機
        if batch_num < total_batches:
            print(f"⏳ 次のバッチまで5秒待機...")
            time.sleep(5)
    
    # 最終サマリー
    print("\n" + "=" * 60)
    print("🎉 全バッチ処理完了！")
    print("=" * 60)
    print("📊 最終統計:")
    print(f"   対象記事数: {len(all_articles)} 件")
    print(f"   注意書き追加: {total_success} 件")
    print(f"   既に追加済み: {total_skip} 件")
    print(f"   エラー: {total_error} 件")
    print(f"   処理済み合計: {total_success + total_skip} 件")
    
    completion_rate = ((total_success + total_skip) / len(all_articles)) * 100
    print(f"   完了率: {completion_rate:.1f}%")
    
    if total_success > 0:
        print(f"\n✨ {total_success} 件の古い記事に注意書きを追加しました！")
        print("すべての1年以上古い記事に適切な注意喚起が設定されました。")

if __name__ == "__main__":
    main()