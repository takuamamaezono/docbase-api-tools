#!/usr/bin/env python3
"""
最終調整：電気一般セクションの残りの商品固有質問を適切なセクションに移動
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

def analyze_remaining_electric_faqs(body):
    """電気一般セクションの残りのFAQを分析"""
    
    # 電気一般セクションを取得
    electric_pattern = r'## ⚡ 電気一般に関する質問.*?</details>'
    electric_match = re.search(electric_pattern, body, re.DOTALL)
    
    if not electric_match:
        print("⚠️ 電気一般セクションが見つかりません")
        return []
    
    electric_content = electric_match.group(0)
    
    # FAQを抽出
    faq_pattern = r'#### Q:\s*([^\n\r]+).*?- \[ \] Web反映対象.*?\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)'
    faqs = re.findall(faq_pattern, electric_content, re.DOTALL)
    
    print(f"🔍 電気一般セクション分析結果:")
    print(f"   現在のFAQ数: {len(faqs)}")
    print()
    
    # 各FAQをチェック
    product_specific = []
    general_electric = []
    
    for question, answer in faqs:
        question = question.strip()
        answer = answer.strip()
        
        # 商品名キーワードをチェック
        product_keywords = ['PowerArQ', 'powerarq', 'mini', 'Mini', 'Solar', 'solar', 'Pro', 'Max', 'S7', 'S10']
        has_product_keyword = any(keyword in question or keyword in answer for keyword in product_keywords)
        
        # 一般的な電気用語をチェック
        general_keywords = ['AC', 'DC', 'PSE', 'バッテリーセル', '電圧', '電流', '周波数', '交流', '直流', 
                           'インバーター', 'コンバーター', 'Hz', 'W数', 'ワット', 'アンペア', 'ボルト',
                           'mAh', 'Wh', 'DoD', 'BMS', '定格', '容量']
        has_general_keyword = any(keyword in question or keyword in answer for keyword in general_keywords)
        
        if has_product_keyword:
            product_specific.append((question, answer))
            print(f"   🔄 商品固有: {question[:50]}...")
        elif has_general_keyword:
            general_electric.append((question, answer))
            print(f"   ✅ 一般電気: {question[:50]}...")
        else:
            print(f"   ❓ 要確認: {question[:50]}...")
    
    print(f"\n📊 分類結果:")
    print(f"   一般的な電気知識: {len(general_electric)}個")
    print(f"   商品固有（要移動）: {len(product_specific)}個")
    
    return product_specific, general_electric

def move_remaining_faqs(body):
    """残りの商品固有FAQを移動"""
    
    product_faqs, general_faqs = analyze_remaining_electric_faqs(body)
    
    if not product_faqs:
        print("✅ 移動が必要なFAQはありません")
        return body
    
    # 電気一般セクションから商品固有FAQを削除し、一般的なFAQのみ残す
    electric_pattern = r'(## ⚡ 電気一般に関する質問.*?)<details>.*?</details>'
    electric_match = re.search(electric_pattern, body, re.DOTALL)
    
    if not electric_match:
        return body
    
    # 一般的な電気FAQで新しいセクションを構築
    new_electric_content = electric_match.group(1) + """<details>
<summary>クリックして展開</summary>

"""
    
    for question, answer in general_faqs:
        new_electric_content += f"""#### Q: {question}
- [ ] Web反映対象
**A:** {answer}

"""
    
    new_electric_content += "</details>"
    
    # 電気一般セクションを更新
    updated_body = body.replace(electric_match.group(0), new_electric_content)
    
    # 商品固有FAQをPowerArQシリーズセクションに移動
    powerarq_pattern = r'(## 🔋 PowerArQシリーズ について.*?)</details>'
    powerarq_match = re.search(powerarq_pattern, updated_body, re.DOTALL)
    
    if powerarq_match:
        powerarq_content = powerarq_match.group(1)
        
        # 商品固有FAQを追加
        for question, answer in product_faqs:
            powerarq_content += f"""

#### Q: {question}
- [ ] Web反映対象
**A:** {answer}"""
        
        new_powerarq_section = powerarq_content + "\n\n</details>"
        updated_body = updated_body.replace(powerarq_match.group(0), new_powerarq_section)
        
        print(f"✅ {len(product_faqs)}個のFAQをPowerArQシリーズセクションに移動しました")
    
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
    
    print("🔧 電気一般セクション最終整理")
    print("=" * 50)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 処理前のFAQ数
    before_electric = len(re.findall(r'#### Q:', re.search(r'## ⚡ 電気一般に関する質問.*?</details>', body, re.DOTALL).group(0) if re.search(r'## ⚡ 電気一般に関する質問.*?</details>', body, re.DOTALL) else ''))
    before_powerarq = len(re.findall(r'#### Q:', re.search(r'## 🔋 PowerArQシリーズ について.*?</details>', body, re.DOTALL).group(0) if re.search(r'## 🔋 PowerArQシリーズ について.*?</details>', body, re.DOTALL) else ''))
    
    print(f"📊 処理前:")
    print(f"   電気一般セクション: {before_electric}個のFAQ")
    print(f"   PowerArQシリーズセクション: {before_powerarq}個のFAQ")
    print()
    
    # FAQの最終整理
    updated_body = move_remaining_faqs(body)
    
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
            print(f"\n🎉 電気一般セクションの最終整理完了！")
            print(f"")
            print(f"📱 完了内容:")
            print(f"   • 電気一般セクションは純粋に一般的な電気知識のみ")
            print(f"   • 商品固有の質問は適切なセクションに配置")
            print(f"   • FAQ構造の整理が完全に完了")
            print(f"")
            print(f"💡 最終確認:")
            print(f"   https://go.docbase.io/posts/{POST_ID}")
    else:
        print(f"\n✅ すでに適切に整理されています")

if __name__ == "__main__":
    main()