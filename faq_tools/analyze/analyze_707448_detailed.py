#!/usr/bin/env python3
"""
記事707448の詳細構造分析とパターン検出
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

def analyze_table_structure(body):
    """テーブル構造を分析"""
    
    # テーブル行のパターンを検索
    table_patterns = {
        'テーブル行（|区切り）': r'\|[^|\n\r]+\|[^|\n\r]+\|',
        'テーブルヘッダー行': r'\|.*質問.*\|.*回答.*\|',
        'FAQ行（質問形式）': r'\|[^|\n\r]*\?[^|\n\r]*\|',
        '大見出し（#）': r'^# [^#\n\r]+',
        'セクション見出し（▼）': r'▼[^\n\r]+',
        'リンク行': r'\[.*\]\(https://.*\)',
    }
    
    results = {}
    for name, pattern in table_patterns.items():
        matches = re.findall(pattern, body, re.MULTILINE)
        results[name] = matches
        print(f"{name}: {len(matches)}個")
        
        # サンプルを表示
        if matches:
            for i, match in enumerate(matches[:3], 1):
                print(f"   {i}. {match[:80]}...")
        print()
    
    return results

def find_faq_sections(body):
    """FAQ形式のセクションを特定"""
    
    # セクションを分割
    sections = re.split(r'^# ', body, flags=re.MULTILINE)
    
    print(f"📋 セクション分析:")
    print(f"   セクション数: {len(sections)}")
    
    faq_sections = []
    
    for i, section in enumerate(sections):
        if not section.strip():
            continue
            
        # セクション名を取得
        lines = section.split('\n')
        section_name = lines[0] if lines else f"セクション{i}"
        
        # テーブル行数をカウント
        table_rows = len(re.findall(r'\|[^|\n\r]+\|[^|\n\r]+\|', section))
        
        print(f"   {i}. {section_name[:50]}... ({table_rows}行のテーブル)")
        
        if table_rows > 0:
            faq_sections.append({
                'index': i,
                'name': section_name,
                'content': section,
                'table_rows': table_rows
            })
    
    return faq_sections

def main():
    TEAM_NAME = "go"
    POST_ID = 707448
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print(f"📄 記事 {POST_ID} の詳細構造分析")
    print("=" * 60)
    
    # 記事を取得
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    print(f"📋 記事情報:")
    print(f"   タイトル: {article_data.get('title', 'N/A')}")
    print(f"   文字数: {len(body):,}文字")
    print()
    
    # テーブル構造分析
    print("🔍 テーブル構造分析")
    print("=" * 40)
    table_results = analyze_table_structure(body)
    
    # セクション分析
    print("📋 セクション分析")
    print("=" * 40)
    faq_sections = find_faq_sections(body)
    
    print(f"\n📊 FAQ形式セクション: {len(faq_sections)}個")
    for section in faq_sections:
        print(f"   • {section['name'][:50]}... ({section['table_rows']}行)")
    
    # サンプルセクションの内容を表示
    if faq_sections:
        print(f"\n📄 サンプルセクション内容:")
        print("-" * 50)
        sample_section = faq_sections[0]
        content_preview = sample_section['content'][:800]
        print(content_preview)
        if len(sample_section['content']) > 800:
            print("...")
        print("-" * 50)
    
    # 対応方針を提案
    print(f"\n💡 対応方針:")
    if table_results['テーブル行（|区切り）']:
        print("   この記事はテーブル形式のFAQです")
        print("   テーブル行に対してフラグを追加する必要があります")
        print("   従来の `#### Q:` 形式とは異なるアプローチが必要です")
    else:
        print("   FAQ構造が特定できませんでした")
        print("   手動での確認と調整が必要です")

if __name__ == "__main__":
    main()