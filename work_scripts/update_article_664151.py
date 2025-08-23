#!/usr/bin/env python3
"""
記事664151にPowerArQ FP600のセクションを追加するスクリプト
"""

import requests
import json
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

def update_article(team_name, access_token, post_id, body):
    """
    記事を更新
    """
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/teams/{team_name}/posts/{post_id}"
    
    data = {
        "body": body,
        "scope": "group"  # ルールに従って従業員のみ（グループ）に設定
    }
    
    try:
        response = requests.patch(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"記事の更新に失敗しました: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"レスポンス: {e.response.text}")
        return None

def main():
    # 記事ID 664151を更新
    TEAM_NAME = "go"
    POST_ID = 664151
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    # 既存の記事内容を読み込む
    with open('/Users/g.ohorudingusu/Docbase/article_664151_backup.json', 'r', encoding='utf-8') as f:
        article = json.load(f)
    
    current_body = article.get('body', '')
    
    # PowerArQ S10 Proのセクションを見つけて、その後にPowerArQ FP600を追加
    # 既存のbodyを行ごとに分割（改行コードを\r\nで統一）
    lines = current_body.replace('\r\n', '\n').split('\n')
    
    # PowerArQ S10 Proセクションの終了位置を探す
    insert_position = -1
    for i, line in enumerate(lines):
        if '## ■PowerArQ S10 Pro' in line:
            # S10 Proセクションから次のセクションまでの位置を探す
            for j in range(i + 1, len(lines)):
                if j < len(lines) - 1 and lines[j].strip() == '' and (lines[j+1].startswith('##') or lines[j+1].startswith('###')):
                    insert_position = j
                    break
    
    if insert_position == -1:
        print("PowerArQ S10 Proセクションが見つかりませんでした")
        return
    
    # PowerArQ FP600のセクションを作成
    fp600_section = [
        "",
        "## ■PowerArQ FP600",
        "| 日付 | SKU | 納品数量 | ロットNo. | 備考 |",
        "| --- | --- | --- | --- | --- |",
        "| 2025年月 | 未定 | 200 | CFST001 | 初回納品 |",
        ""
    ]
    
    # 新しい内容を組み立てる（改行コードを\r\nに戻す）
    new_lines = lines[:insert_position] + fp600_section + lines[insert_position:]
    new_body = '\r\n'.join(new_lines)
    
    print("記事を更新中...")
    result = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, new_body)
    
    if result:
        print("記事の更新が完了しました！")
        print(f"更新日時: {result.get('updated_at', 'N/A')}")
        
        # 更新後の内容を保存
        with open('/Users/g.ohorudingusu/Docbase/article_664151_updated.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    else:
        print("記事の更新に失敗しました")

if __name__ == "__main__":
    main()