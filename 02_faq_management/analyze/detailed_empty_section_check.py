#!/usr/bin/env python3
"""
空のセクションや質問数が少ないセクションを詳細調査
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

def extract_product_sections(body):
    """商品セクションのみを抽出して詳細分析"""
    product_sections = {}
    
    # 商品セクションのパターン（絵文字付きのセクション）
    product_pattern = r'## ([🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]\s*[^#\n\r]+)'
    
    matches = list(re.finditer(product_pattern, body))
    
    for i, match in enumerate(matches):
        section_name = match.group(1).strip()
        start_pos = match.start()
        
        # 次のセクションまでの内容を取得
        if i + 1 < len(matches):
            end_pos = matches[i + 1].start()
        else:
            # 最後のセクションの場合、次の主要セクション（目次以外の##）まで
            remaining_text = body[start_pos:]
            next_main_section = re.search(r'## [^🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]', remaining_text)
            if next_main_section:
                end_pos = start_pos + next_main_section.start()
            else:
                end_pos = len(body)
        
        section_content = body[start_pos:end_pos]
        product_sections[section_name] = section_content
    
    return product_sections

def analyze_section(section_name, section_content):
    """セクションの詳細分析"""
    analysis = {
        'name': section_name,
        'total_length': len(section_content),
        'has_details_tag': '<details>' in section_content,
        'has_questions': False,
        'question_count': 0,
        'questions': [],
        'has_empty_message': False,
        'issues': []
    }
    
    # 空のメッセージをチェック
    empty_patterns = [
        '現在、特定の質問は記載されていません',
        '現在、特定の質問は記載されていません。',
        'よくある質問\n\n現在、特定の質問は記載されていません',
        'よくある質問\r\n\r\n現在、特定の質問は記載されていません'
    ]
    
    for pattern in empty_patterns:
        if pattern in section_content:
            analysis['has_empty_message'] = True
            analysis['issues'].append(f"空のメッセージが含まれています: '{pattern}'")
            break
    
    # 質問を抽出
    question_pattern = r'#### Q:\s*([^\n\r]+)'
    questions = re.findall(question_pattern, section_content)
    
    analysis['question_count'] = len(questions)
    analysis['questions'] = questions
    analysis['has_questions'] = len(questions) > 0
    
    # 問題のあるパターンを特定
    if analysis['has_empty_message']:
        analysis['issues'].append("質問が空になっています")
    elif analysis['question_count'] == 0 and analysis['has_details_tag']:
        analysis['issues'].append("detailsタグはあるが質問が見つかりません")
    elif analysis['question_count'] < 2 and not analysis['has_empty_message']:
        analysis['issues'].append(f"質問数が少なすぎる可能性があります ({analysis['question_count']}個)")
    
    # セクションの長さをチェック
    if analysis['total_length'] < 200:
        analysis['issues'].append("セクションの内容が短すぎる可能性があります")
    
    return analysis

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🔍 空のセクションと質問数の詳細調査を開始します...")
    print("=" * 70)
    
    # 現在の記事を取得
    current_article = get_current_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    if not current_article:
        print("❌ 現在の記事の取得に失敗しました")
        return
    
    current_body = current_article['body']
    
    # 商品セクションを抽出
    product_sections = extract_product_sections(current_body)
    print(f"📦 商品セクション数: {len(product_sections)}")
    print()
    
    # 各セクションを分析
    problematic_sections = []
    empty_sections = []
    low_question_sections = []
    
    for section_name, section_content in product_sections.items():
        analysis = analyze_section(section_name, section_content)
        
        # 問題があるセクションを分類
        if analysis['issues']:
            problematic_sections.append(analysis)
            
            if analysis['has_empty_message']:
                empty_sections.append(analysis)
            elif analysis['question_count'] < 3 and not analysis['has_empty_message']:
                low_question_sections.append(analysis)
    
    # 結果の表示
    print("📊 【調査結果】")
    print(f"   総商品セクション数: {len(product_sections)}")
    print(f"   問題があるセクション数: {len(problematic_sections)}")
    print(f"   完全に空のセクション数: {len(empty_sections)}")
    print(f"   質問数が少ないセクション数: {len(low_question_sections)}")
    print()
    
    if empty_sections:
        print("🚨 【完全に空のセクション】")
        for analysis in empty_sections:
            print(f"   ❌ {analysis['name']}")
            for issue in analysis['issues']:
                print(f"      → {issue}")
        print()
    
    if low_question_sections:
        print("⚠️  【質問数が少ないセクション】")
        for analysis in low_question_sections:
            print(f"   📝 {analysis['name']} ({analysis['question_count']}個の質問)")
            if analysis['questions']:
                for i, q in enumerate(analysis['questions'], 1):
                    print(f"      {i}. {q}")
            for issue in analysis['issues']:
                print(f"      → {issue}")
        print()
    
    # 正常なセクションの統計
    normal_sections = [s for s in product_sections.items() 
                      if not any(analysis['name'] == s[0] for analysis in problematic_sections)]
    
    if normal_sections:
        question_counts = []
        for section_name, section_content in normal_sections:
            questions = re.findall(r'#### Q:', section_content)
            question_counts.append(len(questions))
        
        if question_counts:
            avg_questions = sum(question_counts) / len(question_counts)
            print(f"📈 【正常セクションの統計】")
            print(f"   平均質問数: {avg_questions:.1f}個")
            print(f"   質問数範囲: {min(question_counts)}〜{max(question_counts)}個")
            print()
    
    # 特定の調査：バックアップと比較して内容が大幅に異なるセクション
    print("🔍 【バックアップとの比較調査】")
    try:
        with open('article_backup.json', 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        backup_body = backup_data['body']
        
        backup_sections = extract_product_sections(backup_body)
        
        print(f"   バックアップの商品セクション数: {len(backup_sections)}")
        
        # セクション数の違いをチェック
        missing_in_current = set(backup_sections.keys()) - set(product_sections.keys())
        missing_in_backup = set(product_sections.keys()) - set(backup_sections.keys())
        
        if missing_in_current:
            print(f"   現在の記事にないセクション: {len(missing_in_current)}個")
            for section in missing_in_current:
                print(f"      • {section}")
        
        if missing_in_backup:
            print(f"   バックアップにないセクション: {len(missing_in_backup)}個")
            for section in missing_in_backup:
                print(f"      • {section}")
        
        # 長さが大幅に異なるセクションをチェック
        length_differences = []
        for section_name in set(backup_sections.keys()) & set(product_sections.keys()):
            backup_len = len(backup_sections[section_name])
            current_len = len(product_sections[section_name])
            
            # 50%以上の差がある場合
            if backup_len > 0:
                diff_ratio = abs(current_len - backup_len) / backup_len
                if diff_ratio > 0.5:
                    length_differences.append({
                        'name': section_name,
                        'backup_len': backup_len,
                        'current_len': current_len,
                        'diff_ratio': diff_ratio
                    })
        
        if length_differences:
            print(f"   大幅に長さが変わったセクション: {len(length_differences)}個")
            for diff in sorted(length_differences, key=lambda x: x['diff_ratio'], reverse=True):
                print(f"      • {diff['name']}")
                print(f"        バックアップ: {diff['backup_len']}文字")
                print(f"        現在: {diff['current_len']}文字")
                print(f"        変化率: {diff['diff_ratio']:.1%}")
        
    except FileNotFoundError:
        print("   ⚠️ バックアップファイルが見つかりません")
    
    print()
    print("=" * 70)
    print("✅ 詳細調査が完了しました")

if __name__ == "__main__":
    main()