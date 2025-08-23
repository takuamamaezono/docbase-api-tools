#!/usr/bin/env python3
"""
全FAQに一括でフラグを追加するスクリプト
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

def add_flags_to_all_faqs(body):
    """全商品セクションのFAQにフラグを追加"""
    
    # 商品セクションのパターン（絵文字付きのセクション）
    product_pattern = r'(## [🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]\s*[^#\n\r]+.*?</details>)'
    
    def process_section(match):
        section_content = match.group(1)
        
        # セクション名を取得
        section_name_match = re.search(r'## ([🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]\s*[^#\n\r]+)', section_content)
        section_name = section_name_match.group(1).strip() if section_name_match else "不明"
        
        print(f"📦 処理中: {section_name}")
        
        # FAQを抽出
        q_pattern = r'#### Q:\s*([^\n\r]+)'
        q_matches = list(re.finditer(q_pattern, section_content))
        
        if not q_matches:
            print(f"   FAQが見つかりませんでした")
            return section_content
        
        print(f"   {len(q_matches)}個のFAQを発見")
        
        # セクションヘッダーを保持
        header_match = re.search(r'(## [^#]+.*?よくある質問)', section_content, re.DOTALL)
        if not header_match:
            print(f"   ⚠️ セクション構造が想定と異なります - 手動処理が必要")
            return section_content
        
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
                # セクション終了まで
                q_end = section_content.find('</details>')
                if q_end == -1:
                    q_end = len(section_content)
            
            qa_block = section_content[q_start:q_end]
            
            # 回答を抽出
            answer_match = re.search(r'\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)', qa_block, re.DOTALL)
            answer = answer_match.group(1).strip() if answer_match else ""
            
            # フラグの有無をチェック
            if '- [' in qa_block:
                # 既にフラグがある場合はそのまま
                new_faq = qa_block.strip()
                print(f"   ⏭️ フラグ済み: {question[:40]}...")
            else:
                # フラグがない場合は追加（デフォルト：Web反映対象）
                new_faq = f"""#### Q: {question}
- [ ] Web反映対象
**A:** {answer}"""
                added_flags += 1
                print(f"   ✅ フラグ追加: {question[:40]}...")
            
            new_faqs.append(new_faq)
        
        if added_flags > 0:
            # 新しいセクション内容を構築
            new_section_content = f"{header}\n\n" + "\n\n".join(new_faqs) + f"\n\n{footer}"
            print(f"   📊 {added_flags}個のFAQにフラグを追加しました")
            return new_section_content
        else:
            print(f"   📊 追加するフラグはありませんでした")
            return section_content
    
    # 各商品セクションを処理
    print("🏷️ 全商品セクションにFAQフラグを追加中...")
    print("=" * 60)
    
    updated_body = re.sub(product_pattern, process_section, body, flags=re.DOTALL)
    
    return updated_body

def count_flags_in_body(body):
    """記事内のフラグ数をカウント"""
    target_flags = len(re.findall(r'- \[ \] Web反映対象', body))
    excluded_flags = len(re.findall(r'- \[x\] Web反映除外', body))
    total_faqs = len(re.findall(r'#### Q:', body))
    
    return {
        'total_faqs': total_faqs,
        'target_flags': target_flags,
        'excluded_flags': excluded_flags,
        'flagged_faqs': target_flags + excluded_flags,
        'unflagged_faqs': total_faqs - (target_flags + excluded_flags)
    }

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
    
    print("🚀 全FAQフラグ一括追加システム")
    print("=" * 50)
    
    # 現在の記事を取得
    print("📄 現在の記事を取得中...")
    article_data = get_current_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 処理前のフラグ状況を確認
    print("\n📊 【処理前の状況】")
    before_stats = count_flags_in_body(body)
    print(f"   総FAQ数: {before_stats['total_faqs']}")
    print(f"   フラグ済み: {before_stats['flagged_faqs']}")
    print(f"   未設定: {before_stats['unflagged_faqs']}")
    
    # フラグを追加
    print(f"\n🏷️ フラグ追加処理開始...")
    updated_body = add_flags_to_all_faqs(body)
    
    # 処理後のフラグ状況を確認
    print(f"\n📊 【処理後の状況】")
    after_stats = count_flags_in_body(updated_body)
    print(f"   総FAQ数: {after_stats['total_faqs']}")
    print(f"   フラグ済み: {after_stats['flagged_faqs']}")
    print(f"   Web反映対象: {after_stats['target_flags']}")
    print(f"   Web反映除外: {after_stats['excluded_flags']}")
    print(f"   未設定: {after_stats['unflagged_faqs']}")
    
    # 追加されたフラグ数を計算
    added_flags = after_stats['flagged_faqs'] - before_stats['flagged_faqs']
    
    if added_flags > 0:
        print(f"\n🎯 【変更内容】")
        print(f"   新規追加フラグ: {added_flags}個")
        print(f"   すべて「Web反映対象」として設定")
        
        print(f"\n🔄 Docbaseを更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
        
        if success:
            print(f"\n🎉 全FAQフラグ追加完了！")
            print(f"")
            print(f"📱 Docbase確認ポイント:")
            print(f"   • 各FAQの下に '☐ Web反映対象' が表示される")
            print(f"   • チェックボックス形式で視覚的に確認できる")
            print(f"   • 手動でチェックを入れると '☑ Web反映除外' になる")
            print(f"")
            print(f"🔧 フラグ管理:")
            print(f"   • 除外したいFAQは手動でチェックを入れる")
            print(f"   • python web_sync_filter.py でWeb用データを抽出")
            print(f"   • python faq_flag_manager.py で一括管理")
        
    else:
        print(f"\n⚠️ 新しく追加するフラグはありませんでした")
        print(f"   すべてのFAQに既にフラグが設定されています")

if __name__ == "__main__":
    main()