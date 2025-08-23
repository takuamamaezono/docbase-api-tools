#!/usr/bin/env python3
"""
Web反映用FAQ抽出・フィルタリングシステム
フラグに基づいてWeb反映対象のFAQのみを抽出
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

def extract_web_target_faqs(body):
    """Web反映対象のFAQのみを抽出"""
    
    web_faqs = {
        'sections': [],
        'total_faqs': 0,
        'excluded_count': 0,
        'target_count': 0
    }
    
    # 商品セクションのパターン
    product_pattern = r'## ([🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]\s*[^#\n\r]+)'
    section_matches = list(re.finditer(product_pattern, body))
    
    for i, match in enumerate(section_matches):
        section_name = match.group(1).strip()
        start_pos = match.start()
        
        # 次のセクションまでの内容を取得
        if i + 1 < len(section_matches):
            end_pos = section_matches[i + 1].start()
        else:
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
        
        section_faqs = {
            'name': section_name,
            'target_faqs': [],
            'excluded_faqs': [],
            'unflagged_faqs': []
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
            
            # 回答を抽出
            answer_match = re.search(r'\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)', qa_block, re.DOTALL)
            answer = answer_match.group(1).strip() if answer_match else ""
            
            # フラグの状態をチェック
            if '- [x] Web反映除外' in qa_block:
                section_faqs['excluded_faqs'].append({
                    'question': question,
                    'answer': answer,
                    'reason': 'Web反映除外フラグ'
                })
                web_faqs['excluded_count'] += 1
            elif '- [ ] Web反映対象' in qa_block:
                section_faqs['target_faqs'].append({
                    'question': question,
                    'answer': answer,
                    'flag_status': 'Web反映対象'
                })
                web_faqs['target_count'] += 1
            else:
                # フラグがない場合はデフォルトで対象とする
                section_faqs['unflagged_faqs'].append({
                    'question': question,
                    'answer': answer,
                    'flag_status': 'フラグなし（デフォルト対象）'
                })
                web_faqs['target_count'] += 1
            
            web_faqs['total_faqs'] += 1
        
        if section_faqs['target_faqs'] or section_faqs['excluded_faqs'] or section_faqs['unflagged_faqs']:
            web_faqs['sections'].append(section_faqs)
    
    return web_faqs

def generate_web_content(web_faqs, format_type='json'):
    """Web反映用コンテンツを生成"""
    
    if format_type == 'json':
        # JSON形式で出力
        output = {
            'summary': {
                'total_sections': len(web_faqs['sections']),
                'total_faqs': web_faqs['total_faqs'],
                'target_faqs': web_faqs['target_count'],
                'excluded_faqs': web_faqs['excluded_count']
            },
            'sections': []
        }
        
        for section in web_faqs['sections']:
            section_data = {
                'section_name': section['name'],
                'faqs': []
            }
            
            # Web反映対象のFAQのみを含める
            for faq in section['target_faqs'] + section['unflagged_faqs']:
                section_data['faqs'].append({
                    'question': faq['question'],
                    'answer': faq['answer']
                })
            
            if section_data['faqs']:  # FAQがある場合のみ追加
                output['sections'].append(section_data)
        
        return json.dumps(output, ensure_ascii=False, indent=2)
    
    elif format_type == 'markdown':
        # マークダウン形式で出力（Web反映用）
        content = []
        content.append("# よくある質問（FAQ）")
        content.append("")
        content.append(f"※ Web反映対象: {web_faqs['target_count']}件 / 総FAQ数: {web_faqs['total_faqs']}件")
        content.append("")
        
        for section in web_faqs['sections']:
            target_faqs = section['target_faqs'] + section['unflagged_faqs']
            
            if target_faqs:
                content.append(f"## {section['name']}")
                content.append("")
                
                for faq in target_faqs:
                    content.append(f"### Q: {faq['question']}")
                    content.append(f"**A:** {faq['answer']}")
                    content.append("")
        
        return "\n".join(content)
    
    elif format_type == 'html':
        # HTML形式で出力
        content = []
        content.append("<!DOCTYPE html>")
        content.append("<html lang='ja'>")
        content.append("<head>")
        content.append("    <meta charset='UTF-8'>")
        content.append("    <meta name='viewport' content='width=device-width, initial-scale=1.0'>")
        content.append("    <title>よくある質問（FAQ）</title>")
        content.append("    <style>")
        content.append("        body { font-family: 'Helvetica Neue', Arial, sans-serif; margin: 40px; }")
        content.append("        h1 { color: #333; border-bottom: 2px solid #007bff; }")
        content.append("        h2 { color: #007bff; margin-top: 30px; }")
        content.append("        .faq-item { margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }")
        content.append("        .question { font-weight: bold; color: #333; margin-bottom: 10px; }")
        content.append("        .answer { color: #666; line-height: 1.6; }")
        content.append("        .summary { background: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }")
        content.append("    </style>")
        content.append("</head>")
        content.append("<body>")
        content.append("    <h1>よくある質問（FAQ）</h1>")
        content.append(f"    <div class='summary'>Web反映対象: {web_faqs['target_count']}件 / 総FAQ数: {web_faqs['total_faqs']}件</div>")
        
        for section in web_faqs['sections']:
            target_faqs = section['target_faqs'] + section['unflagged_faqs']
            
            if target_faqs:
                content.append(f"    <h2>{section['name']}</h2>")
                
                for faq in target_faqs:
                    content.append("    <div class='faq-item'>")
                    content.append(f"        <div class='question'>Q: {faq['question']}</div>")
                    content.append(f"        <div class='answer'>A: {faq['answer']}</div>")
                    content.append("    </div>")
        
        content.append("</body>")
        content.append("</html>")
        
        return "\n".join(content)

def generate_exclusion_report(web_faqs):
    """除外されたFAQのレポートを生成"""
    
    report = []
    report.append("# Web反映除外FAQレポート")
    report.append("")
    report.append(f"除外されたFAQ数: {web_faqs['excluded_count']}件")
    report.append("")
    
    for section in web_faqs['sections']:
        if section['excluded_faqs']:
            report.append(f"## {section['name']}")
            report.append("")
            
            for i, faq in enumerate(section['excluded_faqs'], 1):
                report.append(f"### {i}. {faq['question']}")
                report.append(f"**除外理由:** {faq['reason']}")
                report.append(f"**回答:** {faq['answer'][:100]}...")
                report.append("")
    
    return "\n".join(report)

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🌐 Web反映用FAQ抽出システム")
    print("=" * 50)
    
    # 現在の記事を取得
    print("📄 現在の記事を取得中...")
    article_data = get_current_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # Web反映対象FAQを抽出
    print("🔍 Web反映対象FAQを抽出中...")
    web_faqs = extract_web_target_faqs(body)
    
    print(f"\n📊 【抽出結果】")
    print(f"   総FAQ数: {web_faqs['total_faqs']}")
    print(f"   Web反映対象: {web_faqs['target_count']}")
    print(f"   Web反映除外: {web_faqs['excluded_count']}")
    print(f"   対象セクション数: {len(web_faqs['sections'])}")
    
    # 出力形式を選択
    while True:
        print("\n📋 出力形式を選択してください:")
        print("1. JSON形式で出力")
        print("2. Markdown形式で出力")
        print("3. HTML形式で出力")
        print("4. 除外FAQレポートを出力")
        print("5. すべての形式で出力")
        print("6. 終了")
        
        choice = input("\n選択してください (1-6): ").strip()
        
        if choice == '1':
            content = generate_web_content(web_faqs, 'json')
            with open('web_faqs.json', 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ web_faqs.json に出力しました")
        
        elif choice == '2':
            content = generate_web_content(web_faqs, 'markdown')
            with open('web_faqs.md', 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ web_faqs.md に出力しました")
        
        elif choice == '3':
            content = generate_web_content(web_faqs, 'html')
            with open('web_faqs.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ web_faqs.html に出力しました")
        
        elif choice == '4':
            report = generate_exclusion_report(web_faqs)
            with open('excluded_faqs_report.md', 'w', encoding='utf-8') as f:
                f.write(report)
            print("✅ excluded_faqs_report.md に出力しました")
        
        elif choice == '5':
            # すべての形式で出力
            formats = ['json', 'markdown', 'html']
            for fmt in formats:
                content = generate_web_content(web_faqs, fmt)
                filename = f"web_faqs.{fmt if fmt != 'markdown' else 'md'}"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {filename} に出力しました")
            
            # 除外レポートも出力
            report = generate_exclusion_report(web_faqs)
            with open('excluded_faqs_report.md', 'w', encoding='utf-8') as f:
                f.write(report)
            print("✅ excluded_faqs_report.md に出力しました")
        
        elif choice == '6':
            print("👋 終了します")
            break
        
        else:
            print("⚠️ 無効な選択です")

if __name__ == "__main__":
    main()