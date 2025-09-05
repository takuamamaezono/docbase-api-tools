#!/usr/bin/env python3
"""
記事707448の構造を詳細分析
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

def analyze_structure(body):
    """記事構造を詳細分析"""
    
    print("🔍 記事構造の詳細分析")
    print("=" * 50)
    
    # 各種パターンを検索
    patterns = {
        '## セクション（絵文字あり）': r'## [🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]',
        '## セクション（全般）': r'## [^#\n\r]+',
        '### サブセクション': r'### [^#\n\r]+',
        '#### FAQ質問': r'#### Q:',
        'よくある質問見出し': r'### よくある質問',
        'detailsタグ': r'<details>',
        '既存フラグ': r'- \[[ x]\] Web反映',
    }
    
    results = {}
    for name, pattern in patterns.items():
        matches = re.findall(pattern, body)
        results[name] = matches
        print(f"{name}: {len(matches)}個")
        
        # サンプルを表示
        if matches and len(matches) <= 10:
            for i, match in enumerate(matches[:5], 1):
                print(f"   {i}. {match[:50]}...")
        elif len(matches) > 10:
            for i, match in enumerate(matches[:3], 1):
                print(f"   {i}. {match[:50]}...")
            print(f"   ... 他 {len(matches) - 3} 個")
        print()
    
    # 記事の最初の部分を表示
    print("📄 記事開始部分（最初の1000文字）:")
    print("-" * 50)
    print(body[:1000])
    print("-" * 50)
    
    return results

def main():
    TEAM_NAME = "go"
    POST_ID = 707448
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print(f"📄 記事 {POST_ID} の構造分析")
    print("=" * 50)
    
    # 記事を取得
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    print(f"📋 記事情報:")
    print(f"   タイトル: {article_data.get('title', 'N/A')}")
    print(f"   文字数: {len(article_data['body']):,}文字")
    print(f"   更新日: {article_data.get('updated_at', 'N/A')}")
    print()
    
    # 構造分析
    analyze_structure(article_data['body'])

if __name__ == "__main__":
    main()