#!/usr/bin/env python3
"""
FAQ反映フラグ管理システム
各FAQにWeb反映の制御フラグを追加・管理する
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

def extract_faqs_with_flags(section_content):
    """セクションからFAQとフラグ情報を抽出"""
    faqs = []
    
    # #### Q: パターンで質問を検索
    q_pattern = r'#### Q:\s*([^\n\r]+)'
    q_matches = list(re.finditer(q_pattern, section_content))
    
    for i, q_match in enumerate(q_matches):
        question = q_match.group(1).strip()
        q_start = q_match.start()
        
        # 次の質問までの範囲を取得
        if i + 1 < len(q_matches):
            q_end = q_matches[i + 1].start()
        else:
            q_end = len(section_content)
        
        qa_block = section_content[q_start:q_end]
        
        # フラグの有無をチェック
        flag_match = re.search(r'- \[([ x])\]\s*Web反映([対象除外]*)', qa_block)
        
        if flag_match:
            is_excluded = flag_match.group(1) == 'x'
            flag_type = flag_match.group(2)
        else:
            is_excluded = None  # フラグなし
            flag_type = None
        
        # 回答を抽出
        answer_match = re.search(r'\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)', qa_block, re.DOTALL)
        answer = answer_match.group(1).strip() if answer_match else ""
        
        faqs.append({
            'question': question,
            'answer': answer,
            'has_flag': flag_match is not None,
            'is_excluded': is_excluded,
            'flag_type': flag_type,
            'full_block': qa_block.strip()
        })
    
    return faqs

def add_flags_to_faqs(body):
    """すべてのFAQにWeb反映フラグを追加"""
    
    # 商品セクションのパターン
    product_pattern = r'(## [🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]\s*[^#\n\r]+.*?</details>)'
    
    def process_section(match):
        section_content = match.group(1)
        
        # FAQを抽出
        faqs = extract_faqs_with_flags(section_content)
        
        if not faqs:
            return section_content
        
        # セクションヘッダーを保持
        header_match = re.search(r'(## [^#]+.*?### よくある質問)', section_content, re.DOTALL)
        if not header_match:
            return section_content
        
        header = header_match.group(1)
        footer = "</details>"
        
        # フラグ付きFAQを再構築
        new_faqs = []
        for faq in faqs:
            if faq['has_flag']:
                # 既にフラグがある場合はそのまま
                new_faqs.append(faq['full_block'])
            else:
                # フラグがない場合は追加（デフォルト：Web反映対象）
                new_faq = f"""#### Q: {faq['question']}
- [ ] Web反映対象
**A:** {faq['answer']}"""
                new_faqs.append(new_faq)
        
        return f"{header}\n\n" + "\n\n".join(new_faqs) + f"\n\n{footer}"
    
    # 各商品セクションを処理
    updated_body = re.sub(product_pattern, process_section, body, flags=re.DOTALL)
    
    return updated_body

def toggle_faq_flag(body, section_name, question_partial, exclude=True):
    """特定のFAQのフラグを切り替え"""
    
    # セクションを特定
    section_pattern = rf'(## [🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]\s*{re.escape(section_name)}.*?</details>)'
    section_match = re.search(section_pattern, body, re.DOTALL)
    
    if not section_match:
        print(f"⚠️ セクション '{section_name}' が見つかりません")
        return body
    
    section_content = section_match.group(1)
    
    # 質問を部分一致で検索
    question_pattern = rf'(#### Q:\s*[^\n\r]*{re.escape(question_partial)}[^\n\r]*.*?(?=#### Q:|</details>|$))'
    question_match = re.search(question_pattern, section_content, re.DOTALL)
    
    if not question_match:
        print(f"⚠️ 質問 '{question_partial}' が見つかりません")
        return body
    
    qa_block = question_match.group(1)
    
    # フラグの状態を変更
    if exclude:
        # 除外フラグを設定
        if '- [ ] Web反映対象' in qa_block:
            new_qa_block = qa_block.replace('- [ ] Web反映対象', '- [x] Web反映除外')
        elif '- [x] Web反映除外' in qa_block:
            print(f"✅ 質問 '{question_partial}' は既に除外設定されています")
            return body
        else:
            # フラグがない場合は追加
            lines = qa_block.split('\n')
            lines.insert(1, '- [x] Web反映除外')
            new_qa_block = '\n'.join(lines)
    else:
        # 対象フラグを設定
        if '- [x] Web反映除外' in qa_block:
            new_qa_block = qa_block.replace('- [x] Web反映除外', '- [ ] Web反映対象')
        elif '- [ ] Web反映対象' in qa_block:
            print(f"✅ 質問 '{question_partial}' は既に対象設定されています")
            return body
        else:
            # フラグがない場合は追加
            lines = qa_block.split('\n')
            lines.insert(1, '- [ ] Web反映対象')
            new_qa_block = '\n'.join(lines)
    
    # セクション内の質問を置換
    new_section_content = section_content.replace(qa_block, new_qa_block)
    
    # 記事全体を更新
    updated_body = body.replace(section_content, new_section_content)
    
    flag_status = "除外" if exclude else "対象"
    print(f"✅ 質問 '{question_partial}' のフラグを Web反映{flag_status} に変更しました")
    
    return updated_body

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
        faqs = extract_faqs_with_flags(section_content)
        
        if faqs:  # FAQがあるセクションのみを分析
            section_analysis = {
                'name': section_name,
                'total_faqs': len(faqs),
                'flagged_faqs': sum(1 for faq in faqs if faq['has_flag']),
                'excluded_faqs': sum(1 for faq in faqs if faq['is_excluded'] is True),
                'target_faqs': sum(1 for faq in faqs if faq['is_excluded'] is False),
                'unflagged_faqs': sum(1 for faq in faqs if not faq['has_flag']),
                'faqs': faqs
            }
            
            analysis_results['sections'].append(section_analysis)
            analysis_results['total_sections'] += 1
            analysis_results['total_faqs'] += section_analysis['total_faqs']
            analysis_results['flagged_faqs'] += section_analysis['flagged_faqs']
            analysis_results['excluded_faqs'] += section_analysis['excluded_faqs']
            analysis_results['target_faqs'] += section_analysis['target_faqs']
            analysis_results['unflagged_faqs'] += section_analysis['unflagged_faqs']
    
    return analysis_results

def update_article(team_name, access_token, post_id, updated_body):
    """記事を更新"""
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/teams/{team_name}/posts/{post_id}"
    update_data = {"body": updated_body}
    
    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        print("✅ 記事の更新に成功しました！")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ 記事の更新に失敗しました: {e}")
        return False

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🏷️ FAQ反映フラグ管理システム")
    print("=" * 50)
    
    # 現在の記事を取得
    print("📄 現在の記事を取得中...")
    article_data = get_current_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    while True:
        print("\n📋 メニュー:")
        print("1. FAQフラグ状況を分析")
        print("2. すべてのFAQにフラグを追加")
        print("3. 特定のFAQフラグを切り替え")
        print("4. 記事を更新")
        print("5. 終了")
        
        choice = input("\n選択してください (1-5): ").strip()
        
        if choice == '1':
            print("\n🔍 FAQフラグ状況を分析中...")
            analysis = analyze_faq_flags(body)
            
            print(f"\n📊 【分析結果】")
            print(f"   総セクション数: {analysis['total_sections']}")
            print(f"   総FAQ数: {analysis['total_faqs']}")
            print(f"   フラグ付きFAQ: {analysis['flagged_faqs']}")
            print(f"   Web反映除外: {analysis['excluded_faqs']}")
            print(f"   Web反映対象: {analysis['target_faqs']}")
            print(f"   フラグなし: {analysis['unflagged_faqs']}")
            
            for section in analysis['sections']:
                print(f"\n📦 {section['name']}")
                print(f"   FAQ数: {section['total_faqs']}")
                print(f"   除外: {section['excluded_faqs']}, 対象: {section['target_faqs']}, フラグなし: {section['unflagged_faqs']}")
        
        elif choice == '2':
            print("\n🏷️ すべてのFAQにフラグを追加中...")
            body = add_flags_to_faqs(body)
            print("✅ フラグの追加が完了しました")
        
        elif choice == '3':
            section_name = input("セクション名を入力してください（例：ポイントクーラー）: ").strip()
            question_partial = input("質問の一部を入力してください: ").strip()
            exclude_input = input("除外設定しますか？ (y/N): ").strip().lower()
            exclude = exclude_input in ['y', 'yes']
            
            body = toggle_faq_flag(body, section_name, question_partial, exclude)
        
        elif choice == '4':
            confirm = input("記事を更新しますか？ (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, body)
        
        elif choice == '5':
            print("👋 終了します")
            break
        
        else:
            print("⚠️ 無効な選択です")

if __name__ == "__main__":
    main()