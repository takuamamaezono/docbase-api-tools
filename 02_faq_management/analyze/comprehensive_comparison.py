#!/usr/bin/env python3
"""
全商品セクションの質問を詳細比較するスクリプト
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

def extract_questions_from_section(section_text):
    """セクションからQ&Aを抽出"""
    questions = []
    
    # #### Q: パターンで質問を検索
    q_pattern = r'#### Q:\s*([^\n\r]+)'
    a_pattern = r'\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)'
    
    q_matches = re.findall(q_pattern, section_text)
    
    for i, question in enumerate(q_matches):
        # 対応する回答を探す
        q_pos = section_text.find(f'#### Q: {question}')
        if q_pos != -1:
            remaining_text = section_text[q_pos:]
            a_match = re.search(r'\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)', remaining_text, re.DOTALL)
            if a_match:
                answer = a_match.group(1).strip()
                questions.append({
                    'question': question.strip(),
                    'answer': answer.strip()
                })
    
    return questions

def extract_all_sections(body):
    """記事から全セクションを抽出"""
    sections = {}
    
    # セクションの境界を特定するパターン
    section_pattern = r'## ([^#\n\r]+)'
    section_matches = list(re.finditer(section_pattern, body))
    
    for i, match in enumerate(section_matches):
        section_name = match.group(1).strip()
        start_pos = match.start()
        
        # 次のセクションの開始位置を取得
        if i + 1 < len(section_matches):
            end_pos = section_matches[i + 1].start()
        else:
            end_pos = len(body)
        
        section_content = body[start_pos:end_pos]
        sections[section_name] = section_content
    
    return sections

def compare_sections(backup_sections, current_sections):
    """セクション間で質問数と内容を比較"""
    comparison_results = {}
    
    # 商品セクションのキーワード
    product_keywords = [
        'ICEBERG', 'PowerArQ', 'Wearable', 'GearBox', 'PowerBank', 'Electric',
        'FM', 'ポイントクーラー', '冷却ベスト', 'ポータブル発電機', 'シェラカップ'
    ]
    
    for section_name in backup_sections:
        # 商品関連セクションのみをチェック
        is_product_section = any(keyword in section_name for keyword in product_keywords)
        if not is_product_section:
            continue
            
        backup_content = backup_sections[section_name]
        current_content = current_sections.get(section_name, '')
        
        # 質問を抽出
        backup_questions = extract_questions_from_section(backup_content)
        current_questions = extract_questions_from_section(current_content)
        
        # 比較結果を記録
        result = {
            'section_name': section_name,
            'backup_count': len(backup_questions),
            'current_count': len(current_questions),
            'backup_questions': backup_questions,
            'current_questions': current_questions,
            'missing_questions': [],
            'has_changes': False
        }
        
        # 削除された質問を特定
        backup_q_texts = [q['question'] for q in backup_questions]
        current_q_texts = [q['question'] for q in current_questions]
        
        for backup_q in backup_questions:
            if backup_q['question'] not in current_q_texts:
                result['missing_questions'].append(backup_q)
                result['has_changes'] = True
        
        # 質問数が変化している場合は記録
        if len(backup_questions) != len(current_questions) or result['has_changes']:
            comparison_results[section_name] = result
    
    return comparison_results

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🔍 全商品セクションの詳細比較調査を開始します...")
    print("=" * 60)
    
    # バックアップファイルを読み込み
    try:
        with open('article_backup.json', 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        backup_body = backup_data['body']
    except FileNotFoundError:
        print("❌ article_backup.jsonファイルが見つかりません")
        return
    
    # 現在の記事を取得
    current_article = get_current_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    if not current_article:
        print("❌ 現在の記事の取得に失敗しました")
        return
    
    current_body = current_article['body']
    
    print("📊 セクションを抽出中...")
    backup_sections = extract_all_sections(backup_body)
    current_sections = extract_all_sections(current_body)
    
    print(f"バックアップ: {len(backup_sections)} セクション")
    print(f"現在の記事: {len(current_sections)} セクション")
    print()
    
    print("🔍 質問の比較を実行中...")
    comparison_results = compare_sections(backup_sections, current_sections)
    
    # 結果の表示
    if not comparison_results:
        print("✅ 削除された質問は見つかりませんでした。")
        return
    
    print(f"⚠️  {len(comparison_results)} 個のセクションで変更が検出されました:")
    print("=" * 60)
    
    total_missing = 0
    problematic_sections = []
    
    for section_name, result in comparison_results.items():
        print(f"\n📦 【{section_name}】")
        print(f"   バックアップ: {result['backup_count']} 質問")
        print(f"   現在の記事:   {result['current_count']} 質問")
        
        if result['missing_questions']:
            print(f"   ❌ 削除された質問: {len(result['missing_questions'])} 個")
            total_missing += len(result['missing_questions'])
            problematic_sections.append(section_name)
            
            for i, missing_q in enumerate(result['missing_questions'], 1):
                print(f"      {i}. {missing_q['question']}")
                # 回答の一部も表示（長い場合は省略）
                answer_preview = missing_q['answer'][:100]
                if len(missing_q['answer']) > 100:
                    answer_preview += "..."
                print(f"         → {answer_preview}")
        else:
            print("   ✅ 削除された質問はありません")
    
    print()
    print("=" * 60)
    print(f"📈 【調査結果サマリー】")
    print(f"   - 調査対象セクション: {len(comparison_results)} 個")
    print(f"   - 問題のあるセクション: {len(problematic_sections)} 個")
    print(f"   - 削除された質問の総数: {total_missing} 個")
    
    if problematic_sections:
        print(f"\n🚨 復元が必要なセクション:")
        for section in problematic_sections:
            print(f"   • {section}")
    
    # 詳細結果をJSONファイルに保存
    with open('comparison_results.json', 'w', encoding='utf-8') as f:
        json.dump(comparison_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 詳細な比較結果を comparison_results.json に保存しました")

if __name__ == "__main__":
    main()