#!/usr/bin/env python3
"""
バックアップデータの構造を詳しく分析してFAQ数と構造を確認
"""

import json
import re

def analyze_backup_structure():
    """バックアップデータの構造を分析"""
    
    print("🔍 バックアップデータ分析開始...")
    
    with open('/Users/g.ohorudingusu/Docbase/article_backup.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    body = data['body']
    
    print(f"📄 記事タイトル: {data['title']}")
    print(f"📅 最終更新: {data['updated_at']}")
    print(f"📝 本文文字数: {len(body)}")
    
    # セクション構造を分析
    section_pattern = r'## ([🔋⚡🚗💨☀️🔌][^#\n\r]+)'
    sections = re.findall(section_pattern, body)
    
    print(f"\n📋 セクション構造:")
    for i, section in enumerate(sections, 1):
        print(f"   {i:2d}. {section}")
    
    # FAQ数をカウント
    faq_pattern = r'#### Q:'
    total_faqs = len(re.findall(faq_pattern, body))
    
    print(f"\n📊 FAQ総数: {total_faqs}個")
    
    # 各セクションのFAQ数をカウント
    print(f"\n📦 セクション別FAQ数:")
    
    for section in sections:
        # セクション内容を抽出
        section_pattern = rf'## {re.escape(section)}.*?(?=## |$)'
        section_match = re.search(section_pattern, body, re.DOTALL)
        
        if section_match:
            section_content = section_match.group(0)
            section_faqs = len(re.findall(r'#### Q:', section_content))
            print(f"   {section}: {section_faqs}個")
    
    # 特に問題のある部分を詳しく分析
    print(f"\n🔍 FAQ構造の詳細分析:")
    
    # 最初の数個のFAQの構造を確認
    faq_matches = re.finditer(r'#### Q:\s*([^\\n\\r]+).*?(?=#### Q:|</details>|$)', body, re.DOTALL)
    
    for i, match in enumerate(faq_matches):
        if i >= 5:  # 最初の5個だけ
            break
        
        faq_content = match.group(0)
        question_match = re.search(r'#### Q:\s*([^\\n\\r]+)', faq_content)
        question = question_match.group(1) if question_match else "不明"
        
        print(f"   FAQ {i+1}: {question[:50]}...")
        print(f"     内容長: {len(faq_content)}文字")
        
        # 回答部分に「#### Q:」が含まれているかチェック
        answer_part = faq_content[faq_content.find('**A:**'):]
        if '#### Q:' in answer_part:
            print(f"     ⚠️ 回答部分に追加のQ:が含まれています")
    
    return {
        'total_faqs': total_faqs,
        'sections': sections,
        'body': body
    }

if __name__ == "__main__":
    result = analyze_backup_structure()