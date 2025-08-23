#!/usr/bin/env python3
"""
PowerArQ記事をユーザーリクエスト通りに適切に再構成：
1. テーブル形式からdetails形式に変換
2. PowerArQシリーズ全般セクションを作成
3. 各商品セクション（2、Pro、mini2、3、S7、Max、S10 Pro）を独立作成
4. Solarセクションを「(ソーラーパネル)」付きで独立作成
5. 全シリーズのFAQを全般セクションに統合
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

def extract_table_sections_and_faqs(body):
    """テーブル形式のセクションとFAQを抽出・分類"""
    
    print("🔍 テーブル形式のデータを分析中...")
    
    # セクション別に分類するためのデータ構造
    classified_data = {
        'general': [],           # PowerArQシリーズ全般
        'electric': [],          # 電気一般
        'powerarq1': [],         # PowerArQ1
        'powerarq2': [],         # PowerArQ 2
        'powerarq3': [],         # PowerArQ3
        'powerarq_pro': [],      # PowerArQ Pro
        'powerarq_mini': [],     # PowerArQ mini
        'powerarq_mini2': [],    # PowerArQ mini 2
        'powerarq_s7': [],       # PowerArQ S7
        'powerarq_max': [],      # PowerArQ Max
        'powerarq_s10': [],      # PowerArQ S10 Pro
        'solar': []              # Solar（ソーラーパネル）
    }
    
    # テーブル行を抽出（全体から）
    table_pattern = r'\|\s*([^|\n\r]+)\s*\|\s*([^|\n\r]+)\s*\|'
    table_matches = re.findall(table_pattern, body)
    
    print(f"📋 {len(table_matches)}行のテーブルデータを発見")
    
    faq_count = 0
    for question_raw, answer_raw in table_matches:
        # ヘッダー行や区切り行をスキップ
        if ('質問' in question_raw and '回答' in answer_raw) or ('---' in question_raw) or question_raw.strip() == '' or answer_raw.strip() == '':
            continue
        
        # HTMLタグを除去
        question = re.sub(r'<[^>]+>', '', question_raw).strip()
        answer = re.sub(r'<br\s*/?>', '\\n', answer_raw).strip()
        
        # 空の場合はスキップ
        if not question or not answer:
            continue
        
        faq_count += 1
        
        # 質問と回答の内容から分類
        combined_text = (question + " " + answer).lower()
        
        # FAQ項目を作成
        faq_item = {
            'question': question,
            'answer': answer
        }
        
        # 分類ロジック（優先度順）
        if 'solar' in combined_text or 'ソーラー' in combined_text or 'パネル' in combined_text:
            classified_data['solar'].append(faq_item)
            print(f"   ☀️ Solar: {question[:40]}...")
        elif ('powerarq mini2' in combined_text or 'powerarq mini 2' in combined_text or 
              'mini2' in combined_text or 'mini 2' in combined_text):
            classified_data['powerarq_mini2'].append(faq_item)
            print(f"   🔋 PowerArQ mini2: {question[:40]}...")
        elif ('powerarq mini' in combined_text or 'mini' in combined_text):
            classified_data['powerarq_mini'].append(faq_item)
            print(f"   🔋 PowerArQ mini: {question[:40]}...")
        elif ('powerarq3' in combined_text or 'powerarq 3' in combined_text):
            classified_data['powerarq3'].append(faq_item)
            print(f"   🔋 PowerArQ3: {question[:40]}...")
        elif ('powerarq2' in combined_text or 'powerarq 2' in combined_text):
            classified_data['powerarq2'].append(faq_item)
            print(f"   🔋 PowerArQ2: {question[:40]}...")
        elif ('powerarq pro' in combined_text or 'pro' in combined_text):
            classified_data['powerarq_pro'].append(faq_item)
            print(f"   🔋 PowerArQ Pro: {question[:40]}...")
        elif ('powerarq s10' in combined_text or 's10' in combined_text):
            classified_data['powerarq_s10'].append(faq_item)
            print(f"   🔋 PowerArQ S10: {question[:40]}...")
        elif ('powerarq s7' in combined_text or 's7' in combined_text):
            classified_data['powerarq_s7'].append(faq_item)
            print(f"   🔋 PowerArQ S7: {question[:40]}...")
        elif ('powerarq max' in combined_text or 'max' in combined_text):
            classified_data['powerarq_max'].append(faq_item)
            print(f"   🔋 PowerArQ Max: {question[:40]}...")
        elif ('powerarq1' in combined_text or 'powerarq 1' in combined_text):
            classified_data['powerarq1'].append(faq_item)
            print(f"   🔋 PowerArQ1: {question[:40]}...")
        elif ('全シリーズ' in question or '各powerarqシリーズ' in combined_text or 
              'シガーソケット' in combined_text or 'ファン' in combined_text or 
              'w数' in combined_text or '停止する条件' in combined_text or 
              'ランプの色' in combined_text):
            classified_data['general'].append(faq_item)
            print(f"   🔋 全般: {question[:40]}...")
        elif ('電気' in combined_text or 'ac' in combined_text or 'dc' in combined_text or 
              'バッテリー' in combined_text or 'pse' in combined_text or 
              '電圧' in combined_text or '電流' in combined_text):
            classified_data['electric'].append(faq_item)
            print(f"   ⚡ 電気一般: {question[:40]}...")
        else:
            # その他のPowerArQ関連は全般に
            if 'powerarq' in combined_text:
                classified_data['general'].append(faq_item)
                print(f"   🔋 全般（その他）: {question[:40]}...")
            else:
                classified_data['electric'].append(faq_item)
                print(f"   ⚡ 電気一般（その他）: {question[:40]}...")
    
    print(f"\\n📊 分類結果: {faq_count}個のFAQを分類")
    for key, faqs in classified_data.items():
        if faqs:
            print(f"   {key}: {len(faqs)}個")
    
    return classified_data

def create_section_with_faqs(section_name, emoji, faqs):
    """FAQリストからdetails形式のセクションを作成"""
    
    if not faqs:
        return ""
    
    section_content = f"""## {emoji} {section_name}

<details>
<summary>クリックして展開</summary>

"""
    
    for faq in faqs:
        section_content += f"""#### Q: {faq['question']}
- [ ] Web反映対象
**A:** {faq['answer']}

"""
    
    section_content += "</details>"
    
    return section_content

def build_restructured_article(classified_data):
    """分類されたデータから新しい記事構造を構築"""
    
    print("🔧 新しい記事構造を構築中...")
    
    article_parts = [
        """# PowerArQ製品別FAQ - ポータブル電源・ソーラーパネル

## 📋 目次

このページでは、PowerArQポータブル電源とソーラーパネルに関するよくある質問をまとめています。

---

## 🔗 関連リンク

### 全商品のFAQ
- [【SmartTap / PowerArQ】顧客対応FAQ一覧](https://go.docbase.io/posts/1124345)

### 注文番号関連
- [【SmartTap / PowerArQ】注文番号についての説明](https://go.docbase.io/posts/2289424)
- [【SmartTap / PowerArQ】注文番号でお客様情報を検索する方法](https://go.docbase.io/posts/1930308)

### 不具合チェックリスト
- [【PowerArQ】ポータブル電源・ソーラーパネル・ポータブル冷蔵庫の不具合チェックリスト](https://go.docbase.io/posts/1457506)

### その他のFAQ
- [【PowerArQ】製品別FAQ - ポータブル冷蔵庫・サーキュレーター・電気掛敷毛布・シェラカップ](https://go.docbase.io/posts/2705590)
- [【SmartTap】車載ホルダーのFAQ・不具合チェックリスト](https://go.docbase.io/posts/2705677)

### 利用時間早見表
- [楽天カタログ（PDF）](https://www.rakuten.ne.jp/gold/kashima-tokeiten/powerarq_catalog_compression.pdf)

---
"""
    ]
    
    # 各セクションを順番に追加
    sections_config = [
        ('electric', '⚡ 電気一般に関する質問', '⚡'),
        ('general', '🔋 PowerArQシリーズ全般 について', '🔋'),
        ('powerarq1', '🔋 PowerArQ1 について', '🔋'),
        ('powerarq2', '🔋 PowerArQ 2 について', '🔋'),
        ('powerarq3', '🔋 PowerArQ3について', '🔋'),
        ('powerarq_pro', '🔋 PowerArQ Proについて', '🔋'),
        ('powerarq_mini', '🔋 PowerArQ mini について', '🔋'),
        ('powerarq_mini2', '🔋 PowerArQ mini 2について', '🔋'),
        ('powerarq_s7', '🔋 PowerArQ S7について', '🔋'),
        ('powerarq_max', '🔋 PowerArQ Maxについて', '🔋'),
        ('powerarq_s10', '🔋 PowerArQ S10 Proについて', '🔋'),
        ('solar', '🔋 PowerArQ Solar（ソーラーパネル）について', '☀️')
    ]
    
    for key, section_name, emoji in sections_config:
        if key in classified_data and classified_data[key]:
            section_content = create_section_with_faqs(section_name, emoji, classified_data[key])
            if section_content:
                article_parts.append(section_content)
                print(f"   ✅ {section_name}: {len(classified_data[key])}個のFAQ")
    
    return "\\n\\n".join(article_parts)

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
    
    print("🚀 PowerArQ記事再構成システム")
    print("=" * 60)
    print("• テーブル形式からdetails形式に変換")
    print("• PowerArQシリーズ全般セクションを作成")
    print("• 各商品セクションを独立作成")
    print("• Solarセクションを「(ソーラーパネル)」付きで作成")
    print("• 全シリーズFAQを全般セクションに統合")
    print("=" * 60)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 処理前の統計
    before_char_count = len(body)
    before_faq_count = len(re.findall(r'\\|[^\\|\\n\\r]+\\|[^\\|\\n\\r]+\\|', body))
    
    print(f"📊 処理前:")
    print(f"   文字数: {before_char_count:,}文字")
    print(f"   テーブル行数: {before_faq_count}行")
    
    # テーブルデータを抽出・分類
    classified_data = extract_table_sections_and_faqs(body)
    
    # 新しい記事構造を構築
    new_body = build_restructured_article(classified_data)
    
    # 処理後の統計
    after_char_count = len(new_body)
    after_faq_count = len(re.findall(r'#### Q:', new_body))
    after_sections = len(re.findall(r'## [🔋⚡☀️]', new_body))
    
    print(f"\\n📊 処理後:")
    print(f"   文字数: {after_char_count:,}文字")
    print(f"   FAQ数: {after_faq_count}個")
    print(f"   セクション数: {after_sections}個")
    
    # 記事を更新
    print(f"\\n🔄 記事を更新中...")
    success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, new_body)
    
    if success:
        print(f"\\n🎉 PowerArQ記事再構成完了！")
        print(f"")
        print(f"📱 変更内容:")
        print(f"   • テーブル形式からdetails形式に変換")
        print(f"   • PowerArQシリーズ全般セクションを作成")
        print(f"   • 各商品セクション（2, Pro, mini2, 3, S7, Max, S10 Pro）を独立作成")
        print(f"   • Solarセクションを「(ソーラーパネル)」付きで独立作成")
        print(f"   • 全FAQにWeb反映フラグを追加")
        print(f"")
        print(f"💡 確認:")
        print(f"   https://go.docbase.io/posts/{POST_ID}")

if __name__ == "__main__":
    main()