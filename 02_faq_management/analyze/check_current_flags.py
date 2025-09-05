#!/usr/bin/env python3
"""
現在のFAQフラグ状況を確認するスクリプト
"""

import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

def get_current_article(team_name, access_token, post_id):
    """現在の記事内容を取得"""
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

def analyze_faq_flags(body):
    """記事内のFAQフラグ状況を分析"""
    
    # 商品セクションを抽出
    product_pattern = r'## ([🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]\s*[^#\n\r]+)'
    section_matches = list(re.finditer(product_pattern, body))
    
    analysis_results = {
        'total_sections': 0,
        'total_faqs': 0,
        'flagged_faqs': 0,
        'excluded_faqs': 0,
        'target_faqs': 0,
        'unflagged_faqs': 0,
        'sections': []
    }
    
    for i, match in enumerate(section_matches):
        section_name = match.group(1).strip()
        start_pos = match.start()
        
        # 次のセクションまでの内容を取得
        if i + 1 < len(section_matches):
            end_pos = section_matches[i + 1].start()
        else:
            # 最後のセクションの場合
            remaining_text = body[start_pos:]
            next_main_section = re.search(r'## [^🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]', remaining_text)
            if next_main_section:
                end_pos = start_pos + next_main_section.start()
            else:
                end_pos = len(body)
        
        section_content = body[start_pos:end_pos]
        
        # FAQを抽出
        q_pattern = r'#### Q:\s*([^\n\r]+)'
        q_matches = list(re.finditer(q_pattern, section_content))
        
        if q_matches:  # FAQがあるセクションのみを分析
            section_analysis = {
                'name': section_name,
                'total_faqs': len(q_matches),
                'flagged_faqs': 0,
                'excluded_faqs': 0,
                'target_faqs': 0,
                'unflagged_faqs': 0,
                'sample_faqs': []
            }
            
            for j, q_match in enumerate(q_matches):
                question = q_match.group(1).strip()
                q_start = q_match.start()
                
                # 次の質問までの範囲を取得
                if j + 1 < len(q_matches):
                    q_end = q_matches[j + 1].start()
                else:
                    q_end = len(section_content)
                
                qa_block = section_content[q_start:q_end]
                
                # フラグの状態をチェック
                if '- [x] Web反映除外' in qa_block:
                    section_analysis['excluded_faqs'] += 1
                    section_analysis['flagged_faqs'] += 1
                elif '- [ ] Web反映対象' in qa_block:
                    section_analysis['target_faqs'] += 1
                    section_analysis['flagged_faqs'] += 1
                else:
                    section_analysis['unflagged_faqs'] += 1
                
                # サンプルとして最初の3つの質問を保存
                if len(section_analysis['sample_faqs']) < 3:
                    flag_status = "除外" if '- [x] Web反映除外' in qa_block else "対象" if '- [ ] Web反映対象' in qa_block else "フラグなし"
                    section_analysis['sample_faqs'].append({
                        'question': question,
                        'flag_status': flag_status
                    })
            
            analysis_results['sections'].append(section_analysis)
            analysis_results['total_sections'] += 1
            analysis_results['total_faqs'] += section_analysis['total_faqs']
            analysis_results['flagged_faqs'] += section_analysis['flagged_faqs']
            analysis_results['excluded_faqs'] += section_analysis['excluded_faqs']
            analysis_results['target_faqs'] += section_analysis['target_faqs']
            analysis_results['unflagged_faqs'] += section_analysis['unflagged_faqs']
    
    return analysis_results

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🔍 現在のFAQフラグ状況を確認中...")
    print("=" * 50)
    
    # 現在の記事を取得
    article_data = get_current_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # フラグ状況を分析
    analysis = analyze_faq_flags(body)
    
    print(f"\n📊 【FAQフラグ分析結果】")
    print(f"   総セクション数: {analysis['total_sections']}")
    print(f"   総FAQ数: {analysis['total_faqs']}")
    print(f"   フラグ付きFAQ: {analysis['flagged_faqs']}")
    print(f"   Web反映除外: {analysis['excluded_faqs']}")
    print(f"   Web反映対象: {analysis['target_faqs']}")
    print(f"   フラグなし: {analysis['unflagged_faqs']}")
    
    if analysis['unflagged_faqs'] > 0:
        print(f"\n⚠️  まだフラグが設定されていないFAQが {analysis['unflagged_faqs']} 個あります")
        print("   フラグを追加するには: python faq_flag_manager.py を実行")
    
    print(f"\n📝 【セクション詳細】")
    for section in analysis['sections'][:5]:  # 最初の5セクションのみ表示
        print(f"\n📦 {section['name']}")
        print(f"   FAQ数: {section['total_faqs']}")
        print(f"   除外: {section['excluded_faqs']}, 対象: {section['target_faqs']}, フラグなし: {section['unflagged_faqs']}")
        
        if section['sample_faqs']:
            print(f"   サンプル質問:")
            for i, faq in enumerate(section['sample_faqs'], 1):
                print(f"     {i}. {faq['question'][:50]}... [{faq['flag_status']}]")
    
    if len(analysis['sections']) > 5:
        print(f"\n   ... 他 {len(analysis['sections']) - 5} セクション")
    
    print(f"\n💡 Docbase上では以下のように表示されます:")
    print(f"   - [ ] Web反映対象  ← チェックボックス（空）= Web反映する")
    print(f"   - [x] Web反映除外  ← チェックボックス（✓）= Web反映しない")
    print(f"   フラグなし         ← 何も表示されない = デフォルトでWeb反映対象")

if __name__ == "__main__":
    main()