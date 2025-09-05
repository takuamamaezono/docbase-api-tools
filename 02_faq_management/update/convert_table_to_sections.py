#!/usr/bin/env python3
"""
記事707448をテーブル形式からセクション形式に変換
同時にFAQフラグを追加してレイアウトを統一
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

def extract_table_faqs(section_content):
    """テーブル形式のFAQを抽出"""
    
    faqs = []
    
    # テーブル行を抽出（ヘッダー行と区切り行は除外）
    table_rows = re.findall(r'\|\s*([^|\n\r]+)\s*\|\s*([^|\n\r]+)\s*\|', section_content)
    
    for question, answer in table_rows:
        # ヘッダー行や区切り行をスキップ
        if ('質問' in question and '回答' in answer) or ('---' in question) or question.strip() == '' or answer.strip() == '':
            continue
            
        # HTMLタグを除去
        question = re.sub(r'<[^>]+>', '', question).strip()
        answer = re.sub(r'<br\s*/?>', '\n', answer).strip()
        
        # 空の場合はスキップ
        if not question or not answer:
            continue
            
        faqs.append({
            'question': question,
            'answer': answer
        })
    
    return faqs

def convert_section_to_details_format(section_name, section_content):
    """セクションをdetails形式に変換"""
    
    # セクション名から絵文字とクリーンな名前を抽出
    clean_name = re.sub(r'<[^>]+>', '', section_name).strip()
    
    # 適切な絵文字を選択
    emoji_map = {
        '電気一般': '⚡',
        'PowerArQ': '🔋',
        'Solar': '☀️',
        'シガーソケット': '🚗',
        'ファン': '💨',
        '出力': '⚡',
        'ACアダプター': '🔌'
    }
    
    # セクション名に基づいて絵文字を決定
    emoji = '🔋'  # デフォルト
    for keyword, emoji_char in emoji_map.items():
        if keyword in clean_name:
            emoji = emoji_char
            break
    
    # FAQを抽出
    faqs = extract_table_faqs(section_content)
    
    if not faqs:
        print(f"   ⚠️ FAQが見つかりませんでした")
        return None
    
    print(f"   ✅ {len(faqs)}個のFAQを変換")
    
    # details形式のセクションを構築
    details_section = f"""## {emoji} {clean_name}

<details>
<summary>クリックして展開</summary>

"""
    
    # 各FAQを追加
    for faq in faqs:
        details_section += f"""#### Q: {faq['question']}
- [ ] Web反映対象
**A:** {faq['answer']}

"""
    
    details_section += "</details>"
    
    return details_section

def convert_article_structure(body):
    """記事全体をセクション形式に変換"""
    
    print("🔄 記事構造を変換中...")
    print("=" * 50)
    
    # セクションを分割
    sections = re.split(r'^# ', body, flags=re.MULTILINE)
    
    # 変換後の内容を格納
    converted_sections = []
    
    # 最初の部分（目次や関連リンク）を保持
    if sections[0].strip():
        # 関連リンク部分を整理
        intro_content = sections[0].strip()
        
        # 関連リンクを整理
        converted_intro = """# PowerArQ製品別FAQ - ポータブル電源・ソーラーパネル

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
        converted_sections.append(converted_intro)
    
    # 各セクションを処理
    converted_count = 0
    for i, section in enumerate(sections[1:], 1):  # 最初のセクションはスキップ
        if not section.strip():
            continue
        
        # セクション名を取得
        lines = section.split('\n')
        section_name = lines[0] if lines else f"セクション{i}"
        
        print(f"📦 処理中: {section_name[:60]}...")
        
        # テーブルがあるセクションのみ変換
        table_rows = len(re.findall(r'\|[^|\n\r]+\|[^|\n\r]+\|', section))
        
        if table_rows > 2:  # ヘッダー行と区切り行を除いて実際のデータ行があるか
            converted_section = convert_section_to_details_format(section_name, section)
            if converted_section:
                converted_sections.append(converted_section)
                converted_count += 1
        else:
            print(f"   ⏭️ テーブルデータなし - スキップ")
    
    print(f"\n📊 変換結果: {converted_count}セクションを変換しました")
    
    # 変換されたセクションを結合
    return "\n\n".join(converted_sections)

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
    
    print("🔄 記事707448構造変換システム")
    print("=" * 60)
    print("テーブル形式 → セクション形式 + FAQフラグ追加")
    print("=" * 60)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    original_body = article_data['body']
    
    print(f"📋 元記事情報:")
    print(f"   タイトル: {article_data.get('title', 'N/A')}")
    print(f"   文字数: {len(original_body):,}文字")
    
    # テーブル行数をカウント
    table_rows = len(re.findall(r'\|[^|\n\r]+\|[^|\n\r]+\|', original_body))
    print(f"   テーブル行数: {table_rows}行")
    
    # 構造変換を実行
    print(f"\n🔄 構造変換を開始...")
    converted_body = convert_article_structure(original_body)
    
    # 変換後の統計
    converted_faqs = len(re.findall(r'#### Q:', converted_body))
    converted_flags = len(re.findall(r'- \[ \] Web反映対象', converted_body))
    converted_sections = len(re.findall(r'## [🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡☀️🚗🔌]', converted_body))
    
    print(f"\n📊 変換結果:")
    print(f"   変換後FAQ数: {converted_faqs}個")
    print(f"   追加フラグ数: {converted_flags}個")
    print(f"   変換セクション数: {converted_sections}個")
    print(f"   変換後文字数: {len(converted_body):,}文字")
    
    if converted_faqs > 0:
        print(f"\n🔄 記事を更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, converted_body)
        
        if success:
            print(f"\n🎉 記事707448の構造変換完了！")
            print(f"")
            print(f"📱 変更内容:")
            print(f"   • テーブル形式 → セクション形式に変換")
            print(f"   • 全FAQにWeb反映フラグを追加")
            print(f"   • detailsタグでセクションを整理")
            print(f"   • 絵文字付きセクション見出しを追加")
            print(f"   • 統一されたレイアウトを適用")
            print(f"")
            print(f"💡 確認:")
            print(f"   https://go.docbase.io/posts/{POST_ID}")
            print(f"   記事2705590と同じ構造になりました")
    else:
        print(f"\n⚠️ 変換できるFAQが見つかりませんでした")

if __name__ == "__main__":
    main()