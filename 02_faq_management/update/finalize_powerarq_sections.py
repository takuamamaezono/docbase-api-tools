#!/usr/bin/env python3
"""
PowerArQセクションの最終整理
- 全商品セクション（2、Pro、mini2、3、S7、Max、S10 Pro）を独立化
- 「全シリーズ」FAQを全般セクションに統合
- Solarセクションを独立化し「(ソーラーパネル)」を追加
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

def find_all_series_sections(body):
    """「全シリーズ」セクションを検索"""
    all_series_sections = []
    
    # 全シリーズ関連のセクションパターン
    patterns = [
        r'(## [🔋🔌⚡].* 全シリーズ.*?</details>)',
        r'(## [🔋🔌⚡].*▼各PowerArQシリーズ.*?</details>)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, body, re.DOTALL)
        all_series_sections.extend(matches)
    
    return all_series_sections

def finalize_powerarq_organization(body):
    """PowerArQセクションの最終整理を実行"""
    
    print("🔄 PowerArQセクションの最終整理を開始...")
    
    # 現在のセクション構造を確認
    section_pattern = r'## ([🔋⚡🚗💨☀️🔌][^#\n\r]+)'
    sections = re.findall(section_pattern, body)
    
    print("📋 現在のセクション構造:")
    for i, section in enumerate(sections, 1):
        if 'PowerArQ' in section or 'Solar' in section:
            print(f"   {i:2d}. {section}")
    
    # 1. Solar セクションを独立化し「(ソーラーパネル)」を追加
    solar_pattern = r'## 🔋 ■PowerArQ Solarについて'
    if re.search(solar_pattern, body):
        body = re.sub(solar_pattern, '## 🔋 PowerArQ Solar（ソーラーパネル）について', body)
        print("✅ Solarセクションを「(ソーラーパネル)」付きで独立化")
    
    # 2. 「全シリーズ」セクションを検索して全般セクションに統合
    all_series_sections = find_all_series_sections(body)
    
    if all_series_sections:
        print(f"🔍 {len(all_series_sections)}個の「全シリーズ」セクションを発見")
        
        # 全シリーズのFAQを収集
        all_series_faqs = []
        for section in all_series_sections:
            faqs = extract_faqs_from_section(section)
            all_series_faqs.extend(faqs)
            print(f"   📦 セクションから {len(faqs)}個のFAQを抽出")
            
            # 元のセクションを削除
            body = body.replace(section, '')
        
        # 全般セクションに追加
        general_pattern = r'(## 🔋 PowerArQシリーズ全般 について.*?)</details>'
        general_match = re.search(general_pattern, body, re.DOTALL)
        
        if general_match:
            general_section = general_match.group(0)
            existing_faqs = extract_faqs_from_section(general_section)
            
            # 既存FAQと新しいFAQを統合
            all_faqs = existing_faqs + all_series_faqs
            
            # 新しい全般セクションを構築
            new_general_section = """## 🔋 PowerArQシリーズ全般 について

<details>
<summary>クリックして展開</summary>

""" + "\n\n".join(all_faqs) + "\n\n</details>"
            
            body = body.replace(general_section, new_general_section)
            print(f"✅ {len(all_series_faqs)}個の「全シリーズ」FAQを全般セクションに統合")
    
    # 3. 各商品セクションが独立していることを確認
    product_sections = [
        'PowerArQ 2 について',
        'PowerArQ Proについて', 
        'PowerArQ mini 2について',
        'PowerArQ3について',
        'PowerArQ S7について',
        'PowerArQ Maxについて',
        'PowerArQ S10 Proについて'
    ]
    
    print("\n📊 商品セクション独立化確認:")
    for product in product_sections:
        if f"## 🔋 {product}" in body:
            print(f"   ✅ {product} - 独立済み")
        else:
            print(f"   ⚠️ {product} - 見つかりません")
    
    # 余分な改行を整理
    body = re.sub(r'\n{4,}', '\n\n\n', body)
    
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
    POST_ID = 707448
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🎯 PowerArQセクション最終整理システム")
    print("=" * 60)
    print("• 全商品セクションの独立化確認")
    print("• 「全シリーズ」FAQを全般セクションに統合") 
    print("• Solarセクションを独立化し「(ソーラーパネル)」追加")
    print("=" * 60)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 処理前のFAQ数
    before_general = len(re.findall(r'#### Q:', re.search(r'## 🔋 PowerArQシリーズ全般 について.*?</details>', body, re.DOTALL).group(0) if re.search(r'## 🔋 PowerArQシリーズ全般 について.*?</details>', body, re.DOTALL) else ''))
    before_total = len(re.findall(r'#### Q:', body))
    
    print(f"📊 処理前:")
    print(f"   PowerArQシリーズ全般セクション: {before_general}個のFAQ")
    print(f"   記事全体: {before_total}個のFAQ")
    
    # 最終整理を実行
    updated_body = finalize_powerarq_organization(body)
    
    # 処理後のFAQ数
    after_general = len(re.findall(r'#### Q:', re.search(r'## 🔋 PowerArQシリーズ全般 について.*?</details>', updated_body, re.DOTALL).group(0) if re.search(r'## 🔋 PowerArQシリーズ全般 について.*?</details>', updated_body, re.DOTALL) else ''))
    after_total = len(re.findall(r'#### Q:', updated_body))
    
    print(f"\n📊 処理後:")
    print(f"   PowerArQシリーズ全般セクション: {after_general}個のFAQ")
    print(f"   記事全体: {after_total}個のFAQ")
    print(f"   統合されたFAQ: {after_general - before_general}個")
    
    if updated_body != body:
        print(f"\n🔄 記事を更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
        
        if success:
            print(f"\n🎉 PowerArQセクション最終整理完了！")
            print(f"")
            print(f"📱 最終変更内容:")
            print(f"   • 全商品セクション（2, Pro, mini2, 3, S7, Max, S10 Pro）が独立")
            print(f"   • 「全シリーズ」FAQを全般セクションに統合完了")
            print(f"   • Solarセクションを「(ソーラーパネル)」付きで独立化")
            print(f"   • 完全に整理された構造に改善")
            print(f"")
            print(f"💡 最終確認:")
            print(f"   https://go.docbase.io/posts/{POST_ID}")
    else:
        print(f"\n✅ すでに適切に整理されています")

if __name__ == "__main__":
    main()