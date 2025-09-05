#!/usr/bin/env python3
"""
PowerArQシリーズセクションを再編成
- 「PowerArQシリーズ について」→「PowerArQシリーズ全般 について」に変更
- 商品固有のFAQを該当する独立セクションに移動
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
    faq_pattern = r'(#### Q:\s*[^\n\r]+.*?- \[ \] Web反映対象.*?\*\*A:\*\*\s*[^#]*?)(?=####|</details>|$)'
    faqs = re.findall(faq_pattern, section_content, re.DOTALL)
    return [faq.strip() for faq in faqs]

def analyze_powerarq_faqs(faqs):
    """PowerArQシリーズのFAQを分析して分類"""
    
    general_faqs = []
    product_specific_faqs = {
        'PowerArQ1': [],
        'PowerArQ2': [],
        'PowerArQ3': [],
        'PowerArQ Pro': [],
        'PowerArQ mini': [],
        'PowerArQ mini2': [],
        'PowerArQ S7': [],
        'PowerArQ Max': [],
        'PowerArQ S10': [],
        'Solar': []
    }
    
    for faq in faqs:
        # 質問文と回答文を抽出
        question_match = re.search(r'#### Q:\s*([^\n\r]+)', faq)
        question = question_match.group(1) if question_match else ""
        
        answer_match = re.search(r'\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)', faq, re.DOTALL)
        answer = answer_match.group(1) if answer_match else ""
        
        full_text = (question + " " + answer).lower()
        
        # 商品固有キーワードをチェック
        moved = False
        
        # 具体的な商品名をチェック（優先度順）
        if ('powerarq mini2' in full_text or 'powerarq mini 2' in full_text or 
            'mini2' in full_text or 'mini 2' in full_text):
            product_specific_faqs['PowerArQ mini2'].append(faq)
            print(f"   🔄 PowerArQ mini2: {question[:50]}...")
            moved = True
        elif ('powerarq mini' in full_text or 'mini' in full_text) and not moved:
            product_specific_faqs['PowerArQ mini'].append(faq)
            print(f"   🔄 PowerArQ mini: {question[:50]}...")
            moved = True
        elif ('powerarq3' in full_text or 'powerarq 3' in full_text or 
              'powerarq３' in full_text) and not moved:
            product_specific_faqs['PowerArQ3'].append(faq)
            print(f"   🔄 PowerArQ3: {question[:50]}...")
            moved = True
        elif ('powerarq2' in full_text or 'powerarq 2' in full_text or 
              'powerarq２' in full_text) and not moved:
            product_specific_faqs['PowerArQ2'].append(faq)
            print(f"   🔄 PowerArQ2: {question[:50]}...")
            moved = True
        elif ('powerarq pro' in full_text or 'pro' in full_text) and not moved:
            product_specific_faqs['PowerArQ Pro'].append(faq)
            print(f"   🔄 PowerArQ Pro: {question[:50]}...")
            moved = True
        elif ('powerarq s10' in full_text or 's10' in full_text) and not moved:
            product_specific_faqs['PowerArQ S10'].append(faq)
            print(f"   🔄 PowerArQ S10: {question[:50]}...")
            moved = True
        elif ('powerarq s7' in full_text or 's7' in full_text) and not moved:
            product_specific_faqs['PowerArQ S7'].append(faq)
            print(f"   🔄 PowerArQ S7: {question[:50]}...")
            moved = True
        elif ('powerarq max' in full_text or 'max' in full_text) and not moved:
            product_specific_faqs['PowerArQ Max'].append(faq)
            print(f"   🔄 PowerArQ Max: {question[:50]}...")
            moved = True
        elif ('powerarq1' in full_text or 'powerarq 1' in full_text or 
              'powerarq１' in full_text) and not moved:
            product_specific_faqs['PowerArQ1'].append(faq)
            print(f"   🔄 PowerArQ1: {question[:50]}...")
            moved = True
        elif ('solar' in full_text or 'ソーラー' in full_text) and not moved:
            product_specific_faqs['Solar'].append(faq)
            print(f"   🔄 Solar: {question[:50]}...")
            moved = True
        
        if not moved:
            general_faqs.append(faq)
            print(f"   ✅ 全般: {question[:50]}...")
    
    return general_faqs, product_specific_faqs

def reorganize_powerarq_sections(body):
    """PowerArQセクションを再編成"""
    
    print("🔄 PowerArQセクション再編成を開始...")
    
    # PowerArQシリーズセクションを取得
    powerarq_pattern = r'(## 🔋 PowerArQシリーズ について.*?)</details>'
    powerarq_match = re.search(powerarq_pattern, body, re.DOTALL)
    
    if not powerarq_match:
        print("⚠️ PowerArQシリーズセクションが見つかりません")
        return body
    
    powerarq_section = powerarq_match.group(0)
    powerarq_faqs = extract_faqs_from_section(powerarq_section)
    
    print(f"📋 PowerArQシリーズセクションから {len(powerarq_faqs)}個のFAQを抽出")
    
    # FAQを分析・分類
    general_faqs, product_faqs = analyze_powerarq_faqs(powerarq_faqs)
    
    print(f"\n📊 分類結果:")
    print(f"   全般的なFAQ: {len(general_faqs)}個")
    for product, faqs in product_faqs.items():
        if faqs:
            print(f"   {product}: {len(faqs)}個")
    
    # 新しいPowerArQシリーズ全般セクションを作成
    new_general_section = """## 🔋 PowerArQシリーズ全般 について

<details>
<summary>クリックして展開</summary>

""" + "\n\n".join(general_faqs) + "\n\n</details>"
    
    # 元のセクションを置換
    updated_body = body.replace(powerarq_section, new_general_section)
    
    # 各商品セクションにFAQを追加
    section_mappings = {
        'PowerArQ1': r'(## 🔋 PowerArQ1 について.*?)</details>',
        'PowerArQ2': r'(## 🔋 PowerArQ 2 について.*?)</details>',
        'PowerArQ3': r'(## 🔋 PowerArQ3について.*?)</details>',
        'PowerArQ Pro': r'(## 🔋 PowerArQ Proについて.*?)</details>',
        'PowerArQ mini': r'(## 🔋 PowerArQ  mini について.*?)</details>',
        'PowerArQ mini2': r'(## 🔋 PowerArQ mini 2について.*?)</details>',
        'PowerArQ S7': r'(## 🔋 PowerArQ S7について.*?)</details>',
        'PowerArQ Max': r'(## 🔋 PowerArQ Maxについて.*?)</details>',
        'PowerArQ S10': r'(## 🔋 PowerArQ S10 Proについて.*?)</details>',
        'Solar': r'(## 🔋 ■PowerArQ Solarについて.*?)</details>'
    }
    
    for product, faqs_list in product_faqs.items():
        if not faqs_list:
            continue
        
        pattern = section_mappings.get(product)
        if not pattern:
            print(f"   ⚠️ {product}のセクションパターンが見つかりません")
            continue
        
        section_match = re.search(pattern, updated_body, re.DOTALL)
        if not section_match:
            print(f"   ⚠️ {product}セクションが見つかりません")
            continue
        
        target_section = section_match.group(0)
        
        # 既存のFAQを抽出
        existing_faqs = extract_faqs_from_section(target_section)
        
        # 新しいFAQを追加
        all_faqs = existing_faqs + faqs_list
        
        # 新しいセクションを構築
        section_header = target_section.split('</details>')[0].split('<details>')[0]
        new_target_section = section_header + """<details>
<summary>クリックして展開</summary>

""" + "\n\n".join(all_faqs) + "\n\n</details>"
        
        # セクションを更新
        updated_body = updated_body.replace(target_section, new_target_section)
        print(f"   ✅ {product}セクションに {len(faqs_list)}個のFAQを追加しました")
    
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
    
    print("🔄 PowerArQセクション再編成システム")
    print("=" * 60)
    print("PowerArQシリーズ について → PowerArQシリーズ全般 について")
    print("商品固有FAQを各独立セクションに移動")
    print("=" * 60)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 処理前のFAQ数
    before_general = len(re.findall(r'#### Q:', re.search(r'## 🔋 PowerArQシリーズ について.*?</details>', body, re.DOTALL).group(0) if re.search(r'## 🔋 PowerArQシリーズ について.*?</details>', body, re.DOTALL) else ''))
    
    print(f"📊 処理前:")
    print(f"   PowerArQシリーズセクション: {before_general}個のFAQ")
    
    # セクション再編成を実行
    updated_body = reorganize_powerarq_sections(body)
    
    # 処理後のFAQ数
    after_general = len(re.findall(r'#### Q:', re.search(r'## 🔋 PowerArQシリーズ全般 について.*?</details>', updated_body, re.DOTALL).group(0) if re.search(r'## 🔋 PowerArQシリーズ全般 について.*?</details>', updated_body, re.DOTALL) else ''))
    
    print(f"\n📊 処理後:")
    print(f"   PowerArQシリーズ全般セクション: {after_general}個のFAQ")
    print(f"   移動されたFAQ: {before_general - after_general}個")
    
    if updated_body != body:
        print(f"\n🔄 記事を更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
        
        if success:
            print(f"\n🎉 PowerArQセクション再編成完了！")
            print(f"")
            print(f"📱 変更内容:")
            print(f"   • セクション名変更: PowerArQシリーズ について → PowerArQシリーズ全般 について")
            print(f"   • 商品固有FAQを各独立セクションに移動")
            print(f"   • より整理された構造に改善")
            print(f"")
            print(f"💡 確認:")
            print(f"   https://go.docbase.io/posts/{POST_ID}")
    else:
        print(f"\n⚠️ 変更が必要な内容が見つかりませんでした")

if __name__ == "__main__":
    main()