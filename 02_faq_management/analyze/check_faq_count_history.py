#!/usr/bin/env python3
"""
FAQ数の変化を詳しく調査
"""

import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

def get_article(team_name, access_token, post_id):
    """記事内容を取得"""
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/teams/{team_name}/posts/{post_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"記事の取得に失敗しました: {e}")
        return None

def analyze_faq_counts():
    """FAQ数の変化を分析"""
    
    print("📊 FAQ数変化の詳細分析")
    print("=" * 50)
    
    TEAM_NAME = "go"
    POST_ID = 707448
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    # 現在の記事を取得
    current_article = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    if not current_article:
        return
    
    current_body = current_article['body']
    current_faq_count = len(re.findall(r'#### Q:', current_body))
    
    print(f"🔍 現在のFAQ数: {current_faq_count}個")
    
    # セクション別FAQ数をカウント
    sections = [
        ('⚡ 電気一般に関する質問', r'## ⚡ 電気一般に関する質問.*?(?=## |$)'),
        ('🔋 PowerArQシリーズ全般', r'## 🔋 PowerArQシリーズ全般 について.*?(?=## |$)'),
        ('🔋 PowerArQ1', r'## 🔋 PowerArQ1 について.*?(?=## |$)'),
        ('🔋 PowerArQ 2', r'## 🔋 PowerArQ 2 について.*?(?=## |$)'),
        ('🔋 PowerArQ3', r'## 🔋 PowerArQ3について.*?(?=## |$)'),
        ('🔋 PowerArQ Pro', r'## 🔋 PowerArQ Proについて.*?(?=## |$)'),
        ('🔋 PowerArQ mini', r'## 🔋 PowerArQ mini について.*?(?=## |$)'),
        ('🔋 PowerArQ mini 2', r'## 🔋 PowerArQ mini 2について.*?(?=## |$)'),
        ('🔋 PowerArQ S7', r'## 🔋 PowerArQ S7について.*?(?=## |$)'),
        ('🔋 PowerArQ Max', r'## 🔋 PowerArQ Maxについて.*?(?=## |$)'),
        ('🔋 PowerArQ S10 Pro', r'## 🔋 PowerArQ S10 Proについて.*?(?=## |$)'),
        ('☀️ PowerArQ Solar', r'## ☀️ PowerArQ Solar（ソーラーパネル）について.*?(?=## |$)')
    ]
    
    print(f"\n📋 セクション別FAQ数:")
    total_check = 0
    
    for section_name, pattern in sections:
        section_match = re.search(pattern, current_body, re.DOTALL)
        if section_match:
            section_content = section_match.group(0)
            section_faq_count = len(re.findall(r'#### Q:', section_content))
            print(f"   {section_name}: {section_faq_count}個")
            total_check += section_faq_count
        else:
            print(f"   {section_name}: 0個（セクション未発見）")
    
    print(f"\n🔢 合計確認: {total_check}個")
    
    # 変換前の推定FAQ数
    print(f"\n📈 FAQ数の変遷:")
    print(f"   • 変換前（テーブル形式）: 約306個（過去の記録）")
    print(f"   • 変換処理で抽出・分類: 297個")
    print(f"   • 現在のFAQ数: {current_faq_count}個")
    
    if current_faq_count < 306:
        print(f"\n⚠️ FAQ数の減少が確認されました")
        print(f"   減少数: {306 - current_faq_count}個")
        print(f"   減少原因の可能性:")
        print(f"   1. テーブル形式からの変換時にヘッダー行や空行を除外")
        print(f"   2. 重複や不完全なデータの除外")
        print(f"   3. 分類処理で一部のFAQが適切に抽出されなかった")
        
        # 元のテーブル形式のデータがあるかチェック
        print(f"\n🔍 元データの調査が必要な場合:")
        print(f"   • 元のテーブル形式データとの詳細比較")
        print(f"   • 欠落したFAQの特定と復元")
    else:
        print(f"\n✅ FAQ数は適切に維持されています")

if __name__ == "__main__":
    analyze_faq_counts()