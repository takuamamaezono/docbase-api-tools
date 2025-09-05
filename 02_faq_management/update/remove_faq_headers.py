#!/usr/bin/env python3
"""
各セクションから「よくある質問」見出しを削除するスクリプト
"""

import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

def get_current_article(team_name, access_token, post_id):
    """現在の記事内容を取得"""
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

def remove_faq_headers(body):
    """よくある質問の見出しを削除"""
    
    # 様々なパターンの「よくある質問」見出しを削除
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

def preview_changes(original_body, updated_body):
    """変更内容をプレビュー"""
    
    # 変更されたセクションを特定
    original_sections = re.findall(r'## ([🧊❄️💨🛏️🏕️📦🔋🦺🧣🧤📻⚡]\s*[^#\n\r]+)', original_body)
    
    print("📋 変更予定のセクション:")
    for i, section in enumerate(original_sections[:5], 1):  # 最初の5個を表示
        print(f"   {i}. {section}")
    
    if len(original_sections) > 5:
        print(f"   ... 他 {len(original_sections) - 5} セクション")
    
    # サンプル変更を表示
    sample_before = """<summary>クリックして展開</summary>

### よくある質問

#### Q: 質問内容"""
    
    sample_after = """<summary>クリックして展開</summary>

#### Q: 質問内容"""
    
    print(f"\n🔄 変更例:")
    print(f"【変更前】")
    print(sample_before)
    print(f"\n【変更後】")
    print(sample_after)

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("✂️ 「よくある質問」見出し削除システム")
    print("=" * 50)
    
    # 現在の記事を取得
    print("📄 現在の記事を取得中...")
    article_data = get_current_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    original_body = article_data['body']
    
    # 変更内容をプレビュー
    preview_changes(original_body, original_body)
    
    print(f"\n✂️ 「よくある質問」見出しを削除中...")
    updated_body, removed_count = remove_faq_headers(original_body)
    
    if removed_count > 0:
        print(f"📊 {removed_count}個の見出しを削除しました")
        
        # 余分な改行を整理
        print("🧹 余分な改行を整理中...")
        updated_body = clean_extra_linebreaks(updated_body)
        
        print(f"\n🔄 Docbaseを更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
        
        if success:
            print(f"\n🎉 「よくある質問」見出し削除完了！")
            print(f"")
            print(f"📱 変更内容:")
            print(f"   • 各セクションから '### よくある質問' を削除")
            print(f"   • セクション構造がよりスッキリしました")
            print(f"   • FAQフラグは保持されています")
            print(f"")
            print(f"💡 確認方法:")
            print(f"   Docbaseで各セクションを開いて、見出しが削除されているか確認")
        
    else:
        print(f"\n⚠️ 削除対象の見出しが見つかりませんでした")
        print(f"   既に削除済みか、パターンが想定と異なる可能性があります")

if __name__ == "__main__":
    main()