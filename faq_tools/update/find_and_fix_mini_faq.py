#!/usr/bin/env python3
"""
残りのminiに関する質問を適切なセクションに配置
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

def find_all_sections(body):
    """すべてのセクション名を検索"""
    
    # セクション見出しのパターン
    section_pattern = r'## ([🔋⚡🚗💨☀️🔌][^#\n\r]+)'
    sections = re.findall(section_pattern, body)
    
    print("📋 全セクション一覧:")
    for i, section in enumerate(sections, 1):
        print(f"   {i:2d}. {section}")
        if 'mini' in section.lower():
            print(f"       ↑ miniを含むセクション発見！")
    
    return sections

def find_mini_faq_in_electric_section(body):
    """電気一般セクションでminiに関するFAQを検索"""
    
    # 電気一般セクションを取得
    electric_pattern = r'## ⚡ 電気一般に関する質問.*?</details>'
    electric_match = re.search(electric_pattern, body, re.DOTALL)
    
    if not electric_match:
        print("⚠️ 電気一般セクションが見つかりません")
        return None
    
    electric_content = electric_match.group(0)
    
    # miniに関するFAQを検索
    mini_faq_pattern = r'(#### Q:\s*[^#]*?mini[^#]*?\*\*A:\*\*[^#]*?)(?=####|</details>|$)'
    mini_faqs = re.findall(mini_faq_pattern, electric_content, re.DOTALL | re.IGNORECASE)
    
    if mini_faqs:
        print(f"🔍 電気一般セクションでminiに関するFAQ発見: {len(mini_faqs)}個")
        for i, faq in enumerate(mini_faqs, 1):
            question_match = re.search(r'#### Q:\s*([^\n\r]+)', faq)
            question = question_match.group(1) if question_match else "質問不明"
            print(f"   {i}. {question[:60]}...")
    
    return mini_faqs

def move_mini_faq_to_powerarq_section(body):
    """miniに関するFAQをPowerArQシリーズセクションに移動"""
    
    # 移動対象のFAQを検索
    mini_faqs = find_mini_faq_in_electric_section(body)
    
    if not mini_faqs:
        print("⚠️ 移動対象のminiに関するFAQが見つかりません")
        return body
    
    # 電気一般セクションから該当FAQを削除
    electric_pattern = r'(## ⚡ 電気一般に関する質問.*?)</details>'
    electric_match = re.search(electric_pattern, body, re.DOTALL)
    
    if not electric_match:
        return body
    
    electric_content = electric_match.group(1)
    
    # miniに関するFAQを削除
    for faq in mini_faqs:
        electric_content = electric_content.replace(faq, '')
    
    # 余分な改行を整理
    electric_content = re.sub(r'\n{3,}', '\n\n', electric_content)
    
    # 電気一般セクションを更新
    new_electric_section = electric_content + '</details>'
    updated_body = body.replace(electric_match.group(0), new_electric_section)
    
    # PowerArQシリーズセクションに追加
    powerarq_pattern = r'(## 🔋 PowerArQシリーズ について.*?)</details>'
    powerarq_match = re.search(powerarq_pattern, updated_body, re.DOTALL)
    
    if powerarq_match:
        powerarq_content = powerarq_match.group(1)
        
        # miniに関するFAQを追加
        for faq in mini_faqs:
            powerarq_content += "\n\n" + faq.strip()
        
        new_powerarq_section = powerarq_content + "\n\n</details>"
        updated_body = updated_body.replace(powerarq_match.group(0), new_powerarq_section)
        
        print(f"✅ {len(mini_faqs)}個のminiに関するFAQをPowerArQシリーズセクションに移動しました")
    else:
        print("⚠️ PowerArQシリーズセクションが見つかりません")
    
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
    
    print("🔍 miniに関するFAQ移動システム")
    print("=" * 50)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 全セクションを表示
    find_all_sections(body)
    
    print(f"\n🔍 miniに関するFAQを検索中...")
    
    # 処理前のFAQ数
    before_electric = len(re.findall(r'#### Q:', re.search(r'## ⚡ 電気一般に関する質問.*?</details>', body, re.DOTALL).group(0) if re.search(r'## ⚡ 電気一般に関する質問.*?</details>', body, re.DOTALL) else ''))
    before_powerarq = len(re.findall(r'#### Q:', re.search(r'## 🔋 PowerArQシリーズ について.*?</details>', body, re.DOTALL).group(0) if re.search(r'## 🔋 PowerArQシリーズ について.*?</details>', body, re.DOTALL) else ''))
    
    print(f"📊 処理前:")
    print(f"   電気一般セクション: {before_electric}個のFAQ")
    print(f"   PowerArQシリーズセクション: {before_powerarq}個のFAQ")
    
    # FAQの移動処理
    updated_body = move_mini_faq_to_powerarq_section(body)
    
    # 処理後のFAQ数
    after_electric = len(re.findall(r'#### Q:', re.search(r'## ⚡ 電気一般に関する質問.*?</details>', updated_body, re.DOTALL).group(0) if re.search(r'## ⚡ 電気一般に関する質問.*?</details>', updated_body, re.DOTALL) else ''))
    after_powerarq = len(re.findall(r'#### Q:', re.search(r'## 🔋 PowerArQシリーズ について.*?</details>', updated_body, re.DOTALL).group(0) if re.search(r'## 🔋 PowerArQシリーズ について.*?</details>', updated_body, re.DOTALL) else ''))
    
    print(f"\n📊 処理後:")
    print(f"   電気一般セクション: {after_electric}個のFAQ")
    print(f"   PowerArQシリーズセクション: {after_powerarq}個のFAQ")
    print(f"   移動したFAQ: {before_electric - after_electric}個")
    
    if updated_body != body:
        print(f"\n🔄 記事を更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
        
        if success:
            print(f"\n🎉 miniに関するFAQ移動完了！")
            print(f"")
            print(f"📱 変更内容:")
            print(f"   • 電気一般セクションからminiに関するFAQを移動")
            print(f"   • PowerArQシリーズセクションに統合")
            print(f"   • 電気一般セクションは純粋に一般的な電気知識のみに整理完了")
    else:
        print(f"\n⚠️ 移動対象のFAQが見つかりませんでした")

if __name__ == "__main__":
    main()