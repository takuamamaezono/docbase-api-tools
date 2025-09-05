#!/usr/bin/env python3
"""
電気一般セクションから商品固有の質問を適切なセクションに移動
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

def extract_faq_from_section(section_content):
    """セクションからFAQを抽出"""
    faq_pattern = r'(#### Q:\s*[^\n\r]+.*?- \[ \] Web反映対象.*?\*\*A:\*\*\s*[^#]*?)(?=####|</details>|$)'
    faqs = re.findall(faq_pattern, section_content, re.DOTALL)
    return [faq.strip() for faq in faqs]

def reorganize_faqs(body):
    """FAQを適切なセクションに再配置"""
    
    print("🔄 FAQ再配置を開始...")
    
    # 移動対象の質問を定義
    moves = {
        'PowerArQ': [
            'バッテリーセルの個数は？',
            'バッテリーのメーカーは？',
            'ナガジックとは？',
            '「入力」とは？',
            '「出力」とは？',
            '定格容量と定格エネルギーの違いはなんですか？'
        ],
        'PowerArQ2': [
            'オートチャージ機能とは？',
        ],
        'PowerArQ mini': [
            '放電深度（DoD）も考慮して、実質使える電力の計算方法'
        ]
    }
    
    # 電気一般セクションを取得
    electric_pattern = r'(## ⚡ 電気一般に関する質問.*?</details>)'
    electric_match = re.search(electric_pattern, body, re.DOTALL)
    
    if not electric_match:
        print("⚠️ 電気一般セクションが見つかりません")
        return body
    
    electric_section = electric_match.group(1)
    electric_faqs = extract_faq_from_section(electric_section)
    
    print(f"📋 電気一般セクションから {len(electric_faqs)}個のFAQを抽出")
    
    # 移動するFAQと残すFAQを分離
    faqs_to_move = {}
    faqs_to_keep = []
    
    for faq in electric_faqs:
        moved = False
        for target_product, questions in moves.items():
            for question in questions:
                if question in faq:
                    if target_product not in faqs_to_move:
                        faqs_to_move[target_product] = []
                    faqs_to_move[target_product].append(faq)
                    print(f"   🔄 移動対象: {question[:50]}... → {target_product}")
                    moved = True
                    break
            if moved:
                break
        
        if not moved:
            faqs_to_keep.append(faq)
    
    print(f"📊 移動対象: {sum(len(faqs) for faqs in faqs_to_move.values())}個")
    print(f"📊 電気一般に残す: {len(faqs_to_keep)}個")
    
    # 新しい電気一般セクションを構築
    new_electric_section = """## ⚡ 電気一般に関する質問

<details>
<summary>クリックして展開</summary>

""" + "\n\n".join(faqs_to_keep) + "\n\n</details>"
    
    # 電気一般セクションを更新
    updated_body = body.replace(electric_section, new_electric_section)
    
    # 各商品セクションに質問を追加
    for target_product, faqs_list in faqs_to_move.items():
        print(f"\n📦 {target_product}セクションに {len(faqs_list)}個の質問を追加中...")
        
        # セクション名のマッピング
        section_patterns = {
            'PowerArQ': r'(## 🔋 PowerArQシリーズ について.*?</details>)',
            'PowerArQ2': r'(## 🔋 PowerArQ 2 について.*?</details>)',
            'PowerArQ mini': r'(## 🔋 PowerArQ mini について.*?</details>)'
        }
        
        pattern = section_patterns.get(target_product)
        if not pattern:
            print(f"   ⚠️ {target_product}のセクションパターンが見つかりません")
            continue
        
        section_match = re.search(pattern, updated_body, re.DOTALL)
        if not section_match:
            print(f"   ⚠️ {target_product}セクションが見つかりません")
            continue
        
        target_section = section_match.group(1)
        
        # 既存のFAQを抽出
        existing_faqs = extract_faq_from_section(target_section)
        
        # 新しいFAQを追加
        all_faqs = existing_faqs + faqs_list
        
        # 新しいセクションを構築
        section_header = target_section.split('<details>')[0] + '<details>\n<summary>クリックして展開</summary>\n\n'
        new_target_section = section_header + "\n\n".join(all_faqs) + "\n\n</details>"
        
        # セクションを更新
        updated_body = updated_body.replace(target_section, new_target_section)
        print(f"   ✅ {target_product}セクションを更新しました")
    
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
    
    print("🔄 FAQ再配置システム")
    print("=" * 50)
    print("電気一般セクションから商品固有質問を適切なセクションに移動")
    print("=" * 50)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    original_body = article_data['body']
    
    # FAQ数をカウント（処理前）
    before_electric_faqs = len(re.findall(r'#### Q:', re.search(r'## ⚡ 電気一般に関する質問.*?</details>', original_body, re.DOTALL).group(0) if re.search(r'## ⚡ 電気一般に関する質問.*?</details>', original_body, re.DOTALL) else ''))
    before_total_faqs = len(re.findall(r'#### Q:', original_body))
    
    print(f"📊 処理前:")
    print(f"   電気一般セクション: {before_electric_faqs}個のFAQ")
    print(f"   記事全体: {before_total_faqs}個のFAQ")
    
    # FAQ再配置を実行
    updated_body = reorganize_faqs(original_body)
    
    # FAQ数をカウント（処理後）
    after_electric_faqs = len(re.findall(r'#### Q:', re.search(r'## ⚡ 電気一般に関する質問.*?</details>', updated_body, re.DOTALL).group(0) if re.search(r'## ⚡ 電気一般に関する質問.*?</details>', updated_body, re.DOTALL) else ''))
    after_total_faqs = len(re.findall(r'#### Q:', updated_body))
    
    print(f"\n📊 処理後:")
    print(f"   電気一般セクション: {after_electric_faqs}個のFAQ")
    print(f"   記事全体: {after_total_faqs}個のFAQ")
    print(f"   移動した質問: {before_electric_faqs - after_electric_faqs}個")
    
    if updated_body != original_body:
        print(f"\n🔄 記事を更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
        
        if success:
            print(f"\n🎉 FAQ再配置完了！")
            print(f"")
            print(f"📱 変更内容:")
            print(f"   • 電気一般セクションから商品固有質問を移動")
            print(f"   • 各商品セクションに適切な質問を配置")
            print(f"   • 電気一般セクションは純粋に一般的な電気知識のみに")
            print(f"")
            print(f"💡 確認:")
            print(f"   https://go.docbase.io/posts/{POST_ID}")
    else:
        print(f"\n⚠️ 移動する質問が見つかりませんでした")

if __name__ == "__main__":
    main()