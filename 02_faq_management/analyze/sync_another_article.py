#!/usr/bin/env python3
"""
別の記事（707448）に同じフラグ設定とレイアウトを適用
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

def analyze_article_structure(body):
    """記事構造を分析"""
    
    # 商品セクションを検索
    product_pattern = r'## ([🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]\s*[^#\n\r]+)'
    sections = re.findall(product_pattern, body)
    
    # FAQ数をカウント
    total_faqs = len(re.findall(r'#### Q:', body))
    
    # よくある質問見出し数をカウント
    faq_headers = len(re.findall(r'### よくある質問', body))
    
    # 既存フラグ数をカウント
    existing_flags = len(re.findall(r'- \[[ x]\] Web反映', body))
    
    return {
        'sections': sections,
        'total_faqs': total_faqs,
        'faq_headers': faq_headers,
        'existing_flags': existing_flags
    }

def add_flags_to_all_faqs(body):
    """全商品セクションのFAQにフラグを追加"""
    
    # 商品セクションのパターン
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
        
        # セクションヘッダーを保持（よくある質問見出しを除く）
        header_parts = []
        
        # セクション開始からdetailsタグまで
        detail_start = section_content.find('<details>')
        if detail_start == -1:
            print(f"   ⚠️ detailsタグが見つかりません")
            return section_content
            
        # summaryタグまで
        summary_end = section_content.find('</summary>')
        if summary_end == -1:
            print(f"   ⚠️ summaryタグが見つかりません")
            return section_content
            
        header = section_content[:summary_end + len('</summary>')]
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
        
        if added_flags > 0 or q_matches:
            # 新しいセクション内容を構築
            new_section_content = f"{header}\n\n" + "\n\n".join(new_faqs) + f"\n\n{footer}"
            print(f"   📊 {added_flags}個のFAQにフラグを追加しました")
            return new_section_content
        else:
            return section_content
    
    # 各商品セクションを処理
    updated_body = re.sub(product_pattern, process_section, body, flags=re.DOTALL)
    
    return updated_body

def remove_faq_headers(body):
    """よくある質問の見出しを削除"""
    
    patterns_to_remove = [
        r'### よくある質問\n\n',
        r'### よくある質問\r\n\r\n', 
        r'### よくある質問\n',
        r'### よくある質問\r\n',
        r'### よくある質問',
        r'##\s*よくある質問\n\n',
        r'##\s*よくある質問\r\n\r\n',
        r'##\s*よくある質問\n',
        r'##\s*よくある質問\r\n',
        r'##\s*よくある質問',
    ]
    
    updated_body = body
    removed_count = 0
    
    for pattern in patterns_to_remove:
        matches = re.findall(pattern, updated_body)
        if matches:
            updated_body = re.sub(pattern, '', updated_body)
            removed_count += len(matches)
            print(f"✅ パターン '{pattern[:20]}...' で {len(matches)}個削除")
    
    return updated_body, removed_count

def clean_extra_linebreaks(body):
    """余分な改行を整理"""
    
    # 3つ以上連続する改行を2つに統一
    body = re.sub(r'\n{3,}', '\n\n', body)
    body = re.sub(r'\r\n{3,}', '\r\n\r\n', body)
    
    # セクション開始直後の余分な改行を削除
    body = re.sub(r'(<summary>クリックして展開</summary>)\n{3,}', r'\1\n\n', body)
    body = re.sub(r'(<summary>クリックして展開</summary>)\r\n{3,}', r'\1\r\n\r\n', body)
    
    return body

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
    TARGET_POST_ID = 707448  # 対象記事ID
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🔄 記事707448にフラグ設定とレイアウト同期")
    print("=" * 50)
    
    # 対象記事を取得
    print(f"📄 記事 {TARGET_POST_ID} を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, TARGET_POST_ID)
    
    if not article_data:
        return
    
    original_body = article_data['body']
    
    print(f"📋 記事情報:")
    print(f"   タイトル: {article_data.get('title', 'N/A')[:80]}...")
    print(f"   文字数: {len(original_body):,}文字")
    
    # 記事構造を分析
    print(f"\n🔍 記事構造を分析中...")
    analysis = analyze_article_structure(original_body)
    
    print(f"📊 【現在の状況】")
    print(f"   商品セクション数: {len(analysis['sections'])}")
    print(f"   総FAQ数: {analysis['total_faqs']}")
    print(f"   「よくある質問」見出し: {analysis['faq_headers']}個")
    print(f"   既存フラグ: {analysis['existing_flags']}個")
    
    if analysis['sections']:
        print(f"\n📦 商品セクション一覧:")
        for i, section in enumerate(analysis['sections'][:5], 1):
            print(f"   {i}. {section}")
        if len(analysis['sections']) > 5:
            print(f"   ... 他 {len(analysis['sections']) - 5} セクション")
    
    # 処理実行
    updated_body = original_body
    
    # 1. フラグを追加
    if analysis['total_faqs'] > 0:
        print(f"\n🏷️ FAQフラグを追加中...")
        updated_body = add_flags_to_all_faqs(updated_body)
    
    # 2. よくある質問見出しを削除
    if analysis['faq_headers'] > 0:
        print(f"\n✂️ 「よくある質問」見出しを削除中...")
        updated_body, removed_count = remove_faq_headers(updated_body)
        print(f"📊 {removed_count}個の見出しを削除しました")
    
    # 3. 余分な改行を整理
    print(f"\n🧹 レイアウトを整理中...")
    updated_body = clean_extra_linebreaks(updated_body)
    
    # 最終確認
    final_analysis = analyze_article_structure(updated_body)
    
    print(f"\n📊 【処理後の状況】")
    print(f"   総FAQ数: {final_analysis['total_faqs']}")
    print(f"   「よくある質問」見出し: {final_analysis['faq_headers']}個")
    print(f"   フラグ数: {final_analysis['existing_flags']}個")
    
    # 変更があった場合のみ更新
    if updated_body != original_body:
        print(f"\n🔄 記事を更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, TARGET_POST_ID, updated_body)
        
        if success:
            print(f"\n🎉 記事707448の同期完了！")
            print(f"")
            print(f"📱 適用された変更:")
            print(f"   • 全FAQにWeb反映フラグを追加")
            print(f"   • 「よくある質問」見出しを削除")
            print(f"   • レイアウトを整理")
            print(f"")
            print(f"💡 確認:")
            print(f"   https://go.docbase.io/posts/{TARGET_POST_ID}")
    else:
        print(f"\n⚠️ 変更する内容がありませんでした")
        print(f"   記事は既に同期済みの可能性があります")

if __name__ == "__main__":
    main()