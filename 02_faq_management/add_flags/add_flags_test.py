#!/usr/bin/env python3
"""
テスト用：特定のセクションにFAQフラグを追加
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

def add_flags_to_specific_section(body, section_name):
    """特定のセクションにフラグを追加"""
    
    # 指定されたセクションを検索
    section_pattern = rf'(## {re.escape(section_name)}.*?</details>)'
    section_match = re.search(section_pattern, body, re.DOTALL)
    
    if not section_match:
        print(f"⚠️ セクション '{section_name}' が見つかりません")
        return body, 0
    
    section_content = section_match.group(1)
    print(f"📦 セクション '{section_name}' を処理中...")
    
    # FAQを抽出
    q_pattern = r'#### Q:\s*([^\n\r]+)'
    q_matches = list(re.finditer(q_pattern, section_content))
    
    if not q_matches:
        print(f"   FAQが見つかりませんでした")
        return body, 0
    
    print(f"   {len(q_matches)}個のFAQを発見")
    
    # セクションヘッダーを保持
    header_match = re.search(r'(## [^#]+.*?### よくある質問)', section_content, re.DOTALL)
    if not header_match:
        print(f"   セクション構造が想定と異なります")
        return body, 0
    
    header = header_match.group(1)
    footer = "</details>"
    
    # フラグ付きFAQを再構築
    new_faqs = []
    added_flags = 0
    
    for i, q_match in enumerate(q_matches):
        question = q_match.group(1).strip()
        q_start = q_match.start()
        
        # 次の質問までの範囲を取得
        if i + 1 < len(q_matches):
            q_end = q_matches[i + 1].start()
        else:
            q_end = len(section_content)
        
        qa_block = section_content[q_start:q_end]
        
        # 回答を抽出
        answer_match = re.search(r'\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)', qa_block, re.DOTALL)
        answer = answer_match.group(1).strip() if answer_match else ""
        
        # フラグがない場合は追加（デフォルト：Web反映対象）
        if '- [' not in qa_block:
            new_faq = f"""#### Q: {question}
- [ ] Web反映対象
**A:** {answer}"""
            added_flags += 1
            print(f"   ✅ フラグ追加: {question[:50]}...")
        else:
            # 既にフラグがある場合はそのまま
            new_faq = qa_block.strip()
            print(f"   ⏭️ フラグ済み: {question[:50]}...")
        
        new_faqs.append(new_faq)
    
    # 新しいセクション内容を構築
    new_section_content = f"{header}\n\n" + "\n\n".join(new_faqs) + f"\n\n{footer}"
    
    # 記事全体を更新
    updated_body = body.replace(section_content, new_section_content)
    
    print(f"   📊 {added_flags}個のFAQにフラグを追加しました")
    
    return updated_body, added_flags

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
    
    print("🏷️ FAQ反映フラグ追加テスト")
    print("=" * 50)
    
    # 現在の記事を取得
    print("📄 現在の記事を取得中...")
    article_data = get_current_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # テスト対象のセクション（小さめのセクションから開始）
    test_sections = [
        "❄️ ポイントクーラー",
        "🦺 冷却ベスト", 
        "🏕️ PowerArQ シェラカップ"
    ]
    
    total_added = 0
    updated_body = body
    
    for section_name in test_sections:
        updated_body, added_count = add_flags_to_specific_section(updated_body, section_name)
        total_added += added_count
    
    if total_added > 0:
        print(f"\n📊 【処理結果】")
        print(f"   総追加フラグ数: {total_added}個")
        print(f"   処理セクション数: {len(test_sections)}個")
        
        print(f"\n🔄 Docbaseを更新しますか？")
        print(f"   更新すると、Docbase上でチェックボックスが表示されます")
        
        # 自動で更新
        print(f"   更新を実行中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
        
        if success:
            print(f"\n🎉 テスト完了！")
            print(f"   Docbaseでチェックボックスが表示されているか確認してください")
            print(f"")
            print(f"💡 確認方法:")
            print(f"   1. Docbaseの記事を開く")
            print(f"   2. 以下のセクションを確認:")
            for section in test_sections:
                print(f"      - {section}")
            print(f"   3. 各FAQの下に '☐ Web反映対象' が表示されていればOK")
            print(f"")
            print(f"🚀 全セクションに適用する場合:")
            print(f"   python faq_flag_manager.py を実行してメニュー2を選択")
        
    else:
        print(f"\n⚠️ フラグを追加するFAQが見つかりませんでした")

if __name__ == "__main__":
    main()