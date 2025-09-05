#!/usr/bin/env python3
"""
記事の表示問題を修正：
- セクション名の絵文字重複を修正
- その他の表示問題をチェック・修正
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

def fix_display_issues(body):
    """表示問題を修正"""
    
    print("🔧 表示問題の修正を開始...")
    
    fixed_body = body
    fixes_applied = []
    
    # 1. セクション名の絵文字重複を修正
    emoji_duplicates = [
        (r'## ⚡ ⚡ 電気一般に関する質問', '## ⚡ 電気一般に関する質問'),
        (r'## 🔋 🔋 PowerArQシリーズ全般 について', '## 🔋 PowerArQシリーズ全般 について'),
        (r'## 🔋 🔋 PowerArQ1 について', '## 🔋 PowerArQ1 について'),
        (r'## 🔋 🔋 PowerArQ 2 について', '## 🔋 PowerArQ 2 について'),
        (r'## 🔋 🔋 PowerArQ3について', '## 🔋 PowerArQ3について'),
        (r'## 🔋 🔋 PowerArQ Proについて', '## 🔋 PowerArQ Proについて'),
        (r'## 🔋 🔋 PowerArQ mini について', '## 🔋 PowerArQ mini について'),
        (r'## 🔋 🔋 PowerArQ mini 2について', '## 🔋 PowerArQ mini 2について'),
        (r'## 🔋 🔋 PowerArQ S7について', '## 🔋 PowerArQ S7について'),
        (r'## 🔋 🔋 PowerArQ Maxについて', '## 🔋 PowerArQ Maxについて'),
        (r'## 🔋 🔋 PowerArQ S10 Proについて', '## 🔋 PowerArQ S10 Proについて'),
        (r'## ☀️ 🔋 PowerArQ Solar（ソーラーパネル）について', '## ☀️ PowerArQ Solar（ソーラーパネル）について')
    ]
    
    for wrong_pattern, correct_text in emoji_duplicates:
        if re.search(wrong_pattern, fixed_body):
            fixed_body = re.sub(wrong_pattern, correct_text, fixed_body)
            fixes_applied.append(f"絵文字重複修正: {wrong_pattern} → {correct_text}")
            print(f"   ✅ 修正: {correct_text}")
    
    # 2. エスケープ文字の修正
    escape_fixes = [
        (r'\\n\\n', '\n\n'),
        (r'\\n', '\n'),
        (r'\\', '')
    ]
    
    for wrong, correct in escape_fixes:
        if wrong in fixed_body:
            fixed_body = fixed_body.replace(wrong, correct)
            fixes_applied.append(f"エスケープ文字修正: {wrong} → {correct}")
    
    # 3. 余分な改行の整理
    fixed_body = re.sub(r'\n{4,}', '\n\n\n', fixed_body)
    
    # 4. FAQの質問部分で不適切な改行がないかチェック
    faq_pattern = r'#### Q:\s*([^\n\r]*?)(\n- \[ \] Web反映対象)'
    faqs = re.finditer(faq_pattern, fixed_body)
    
    for match in faqs:
        question = match.group(1).strip()
        if '...' in question and len(question) < 10:
            print(f"   ⚠️ 短縮された質問を発見: {question}")
    
    # 5. リンクや特殊文字の修正
    link_fixes = [
        (r'【https://www\.meti\.go\.jp/policy/consumer/seian/denan/mlb_faq\.html', '【https://www.meti.go.jp/policy/consumer/seian/denan/mlb_faq.html】')
    ]
    
    for wrong, correct in link_fixes:
        if re.search(wrong, fixed_body):
            fixed_body = re.sub(wrong, correct, fixed_body)
            fixes_applied.append(f"リンク修正")
    
    print(f"\n📊 修正適用数: {len(fixes_applied)}件")
    if fixes_applied:
        for fix in fixes_applied[:5]:  # 最初の5件を表示
            print(f"   • {fix}")
        if len(fixes_applied) > 5:
            print(f"   • その他 {len(fixes_applied) - 5}件")
    
    return fixed_body

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
    
    print("🔧 記事表示問題修正システム")
    print("=" * 50)
    print("• セクション名の絵文字重複を修正")
    print("• エスケープ文字を修正")
    print("• その他の表示問題を修正")
    print("=" * 50)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 処理前の統計
    before_char_count = len(body)
    before_sections = len(re.findall(r'## [⚡🔋☀️]', body))
    
    print(f"📊 処理前:")
    print(f"   文字数: {before_char_count:,}文字")
    print(f"   セクション数: {before_sections}個")
    
    # 表示問題を修正
    fixed_body = fix_display_issues(body)
    
    # 処理後の統計
    after_char_count = len(fixed_body)
    after_sections = len(re.findall(r'## [⚡🔋☀️]', fixed_body))
    
    print(f"\n📊 処理後:")
    print(f"   文字数: {after_char_count:,}文字")
    print(f"   セクション数: {after_sections}個")
    
    if fixed_body != body:
        print(f"\n🔄 記事を更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, fixed_body)
        
        if success:
            print(f"\n🎉 表示問題修正完了！")
            print(f"")
            print(f"📱 修正内容:")
            print(f"   • セクション名の絵文字重複を修正")
            print(f"   • エスケープ文字を修正")
            print(f"   • リンクや特殊文字を修正")
            print(f"")
            print(f"💡 確認:")
            print(f"   https://go.docbase.io/posts/{POST_ID}")
    else:
        print(f"\n✅ 修正が必要な問題は見つかりませんでした")

if __name__ == "__main__":
    main()