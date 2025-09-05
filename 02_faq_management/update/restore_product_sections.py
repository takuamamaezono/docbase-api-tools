#!/usr/bin/env python3
"""
消失した商品別セクションを復元し、PowerArQ全般セクションのFAQを適切に分類
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

def extract_faqs_from_section(section_content):
    """セクションからFAQを抽出"""
    faq_pattern = r'(#### Q:\s*[^\\n\\r]+.*?- \[ \] Web反映対象.*?\*\*A:\*\*\s*[^#]*?)(?=####|</details>|$)'
    faqs = re.findall(faq_pattern, section_content, re.DOTALL)
    return [faq.strip() for faq in faqs]

def analyze_and_classify_faqs(faqs):
    """FAQを分析して商品別に分類"""
    
    classified_faqs = {
        'PowerArQ全般': [],
        'PowerArQ1': [],
        'PowerArQ2': [],
        'PowerArQ3': [],
        'PowerArQ Pro': [],
        'PowerArQ mini': [],
        'PowerArQ mini2': [],
        'PowerArQ S7': [],
        'PowerArQ Max': [],
        'PowerArQ S10': []
    }
    
    for faq in faqs:
        # 質問文と回答文を抽出
        question_match = re.search(r'#### Q:\s*([^\\n\\r]+)', faq)
        question = question_match.group(1) if question_match else ""
        
        answer_match = re.search(r'\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)', faq, re.DOTALL)
        answer = answer_match.group(1) if answer_match else ""
        
        full_text = (question + " " + answer).lower()
        
        # 商品固有キーワードをチェック（優先度順）
        classified = False
        
        # 具体的な商品名をチェック
        if ('powerarq mini2' in full_text or 'powerarq mini 2' in full_text or 
            'mini2' in full_text or 'mini 2' in full_text):
            classified_faqs['PowerArQ mini2'].append(faq)
            print(f"   🔄 PowerArQ mini2: {question[:50]}...")
            classified = True
        elif ('powerarq mini' in full_text or 'mini' in full_text) and not classified:
            classified_faqs['PowerArQ mini'].append(faq)
            print(f"   🔄 PowerArQ mini: {question[:50]}...")
            classified = True
        elif ('powerarq3' in full_text or 'powerarq 3' in full_text or 
              'powerarq３' in full_text) and not classified:
            classified_faqs['PowerArQ3'].append(faq)
            print(f"   🔄 PowerArQ3: {question[:50]}...")
            classified = True
        elif ('powerarq2' in full_text or 'powerarq 2' in full_text or 
              'powerarq２' in full_text) and not classified:
            classified_faqs['PowerArQ2'].append(faq)
            print(f"   🔄 PowerArQ2: {question[:50]}...")
            classified = True
        elif ('powerarq pro' in full_text or 'pro' in full_text) and not classified:
            classified_faqs['PowerArQ Pro'].append(faq)
            print(f"   🔄 PowerArQ Pro: {question[:50]}...")
            classified = True
        elif ('powerarq s10' in full_text or 's10' in full_text) and not classified:
            classified_faqs['PowerArQ S10'].append(faq)
            print(f"   🔄 PowerArQ S10: {question[:50]}...")
            classified = True
        elif ('powerarq s7' in full_text or 's7' in full_text) and not classified:
            classified_faqs['PowerArQ S7'].append(faq)
            print(f"   🔄 PowerArQ S7: {question[:50]}...")
            classified = True
        elif ('powerarq max' in full_text or 'max' in full_text) and not classified:
            classified_faqs['PowerArQ Max'].append(faq)
            print(f"   🔄 PowerArQ Max: {question[:50]}...")
            classified = True
        elif ('powerarq1' in full_text or 'powerarq 1' in full_text or 
              'powerarq１' in full_text) and not classified:
            classified_faqs['PowerArQ1'].append(faq)
            print(f"   🔄 PowerArQ1: {question[:50]}...")
            classified = True
        
        if not classified:
            classified_faqs['PowerArQ全般'].append(faq)
            print(f"   ✅ 全般: {question[:50]}...")
    
    return classified_faqs

def restore_product_sections(body):
    """商品別セクションを復元"""
    
    print("🔄 商品別セクション復元を開始...")
    
    # 現在統合されている全PowerArQシリーズセクションを取得
    # 「▼各PowerArQシリーズ」セクションからFAQを取得
    series_patterns = [
        r'## 🔋 ▼各PowerArQシリーズ 自動で出力が停止する条件.*?</details>',
        r'## 🔋 ▼各PowerArQシリーズ　ACアダプターのランプの色.*?</details>'
    ]
    
    all_faqs = []
    sections_found = []
    
    for pattern in series_patterns:
        match = re.search(pattern, body, re.DOTALL)
        if match:
            section = match.group(0)
            sections_found.append(section)
            faqs = extract_faqs_from_section(section)
            all_faqs.extend(faqs)
            print(f"📦 セクションから {len(faqs)}個のFAQを抽出")
    
    if not sections_found:
        print("⚠️ PowerArQシリーズセクションが見つかりません")
        return body
    
    print(f"📋 PowerArQシリーズセクションから {len(all_faqs)}個のFAQを抽出")
    
    # FAQを分析・分類
    classified_faqs = analyze_and_classify_faqs(all_faqs)
    
    print(f"\\n📊 分類結果:")
    for product, faqs in classified_faqs.items():
        if faqs:
            print(f"   {product}: {len(faqs)}個")
    
    # 新しい全般セクションを作成（全般のFAQのみ）
    new_general_section = """## 🔋 PowerArQシリーズ全般 について

<details>
<summary>クリックして展開</summary>

""" + "\\n\\n".join(classified_faqs['PowerArQ全般']) + "\\n\\n</details>"
    
    # 元の「▼各PowerArQシリーズ」セクションを削除して新しい全般セクションに置換
    updated_body = body
    for section in sections_found:
        updated_body = updated_body.replace(section, '', 1)  # 最初の1つだけ削除
    
    # 最初の「全シリーズ」セクションの場所に新しい全般セクションを挿入
    if sections_found:
        first_section_pos = body.find(sections_found[0])
        updated_body = updated_body[:first_section_pos] + new_general_section + updated_body[first_section_pos:]
    
    # 各商品セクションを作成・挿入
    product_sections = [
        ('PowerArQ1', '## 🔋 PowerArQ1 について'),
        ('PowerArQ2', '## 🔋 PowerArQ 2 について'),
        ('PowerArQ3', '## 🔋 PowerArQ3について'),
        ('PowerArQ Pro', '## 🔋 PowerArQ Proについて'),
        ('PowerArQ mini', '## 🔋 PowerArQ mini について'),
        ('PowerArQ mini2', '## 🔋 PowerArQ mini 2について'),
        ('PowerArQ S7', '## 🔋 PowerArQ S7について'),
        ('PowerArQ Max', '## 🔋 PowerArQ Maxについて'),
        ('PowerArQ S10', '## 🔋 PowerArQ S10 Proについて')
    ]
    
    # 新しい商品セクションを全般セクションの後に追加
    insertion_point = updated_body.find(new_general_section) + len(new_general_section)
    
    new_sections = []
    for product_key, section_title in product_sections:
        if classified_faqs[product_key]:
            section_content = f"""

{section_title}

<details>
<summary>クリックして展開</summary>

""" + "\\n\\n".join(classified_faqs[product_key]) + "\\n\\n</details>"
            new_sections.append(section_content)
            print(f"✅ {product_key}セクションを作成: {len(classified_faqs[product_key])}個のFAQ")
    
    # 新しいセクションを挿入
    updated_body = updated_body[:insertion_point] + "".join(new_sections) + updated_body[insertion_point:]
    
    return updated_body

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
    POST_ID = 707448
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🔧 PowerArQ商品別セクション復元システム")
    print("=" * 60)
    print("• PowerArQ全般セクションのFAQを分析")
    print("• 商品固有FAQを特定し適切なセクションに分類")
    print("• 各商品の独立セクションを再作成")
    print("=" * 60)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 処理前のセクション数とFAQ数
    before_sections = len(re.findall(r'## 🔋.*について', body))
    before_total_faqs = len(re.findall(r'#### Q:', body))
    
    print(f"📊 処理前:")
    print(f"   PowerArQセクション数: {before_sections}個")
    print(f"   FAQ総数: {before_total_faqs}個")
    
    # 商品別セクション復元を実行
    updated_body = restore_product_sections(body)
    
    # 処理後のセクション数とFAQ数
    after_sections = len(re.findall(r'## 🔋.*について', updated_body))
    after_total_faqs = len(re.findall(r'#### Q:', updated_body))
    
    print(f"\\n📊 処理後:")
    print(f"   PowerArQセクション数: {after_sections}個")
    print(f"   FAQ総数: {after_total_faqs}個")
    print(f"   復元されたセクション: {after_sections - before_sections}個")
    
    if updated_body != body:
        print(f"\\n🔄 記事を更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
        
        if success:
            print(f"\\n🎉 商品別セクション復元完了！")
            print(f"")
            print(f"📱 変更内容:")
            print(f"   • PowerArQ全般セクションから商品固有FAQを分離")
            print(f"   • 各商品の独立セクションを再作成")
            print(f"   • 適切なFAQ分類により整理された構造")
            print(f"")
            print(f"💡 確認:")
            print(f"   https://go.docbase.io/posts/{POST_ID}")
    else:
        print(f"\\n⚠️ 処理対象のFAQが見つかりませんでした")

if __name__ == "__main__":
    main()