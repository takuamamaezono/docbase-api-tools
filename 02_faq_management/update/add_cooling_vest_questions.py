#!/usr/bin/env python3
"""
冷却ベストの質問を追加するスクリプト
"""

import requests
import json
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

def get_current_article(team_name, access_token, post_id):
    """
    現在の記事内容を取得
    """
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

def update_article(team_name, access_token, post_id, updated_body):
    """
    記事を更新する
    """
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/teams/{team_name}/posts/{post_id}"
    
    update_data = {
        "body": updated_body
    }
    
    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        print("✅ 記事の更新に成功しました！")
        print(f"更新日時: {response.json().get('updated_at', 'N/A')}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ 記事の更新に失敗しました: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"エラー詳細: {e.response.text}")
        return False

def add_cooling_vest_questions(body):
    """
    冷却ベストの質問を追加
    """
    # 様々な改行パターンに対応
    patterns_to_replace = [
        "## 🦺 冷却ベスト\n\n<details>\n<summary>クリックして展開</summary>\n\n### よくある質問\n\n現在、特定の質問は記載されていません。\n\n</details>",
        "## 🦺 冷却ベスト\r\n\r\n<details>\r\n<summary>クリックして展開</summary>\r\n\r\n### よくある質問\r\n\r\n現在、特定の質問は記載されていません。\r\n\r\n</details>",
        "## 🦺 冷却ベスト\n\n<details>\n<summary>クリックして展開</summary>\n\n現在、特定の質問は記載されていません。\n\n</details>",
        "## 🦺 冷却ベスト\r\n\r\n<details>\r\n<summary>クリックして展開</summary>\r\n\r\n現在、特定の質問は記載されていません。\r\n\r\n</details>"
    ]

    # 冷却ベストの質問を追加
    cooling_vest_with_questions = """## 🦺 冷却ベスト

<details>
<summary>クリックして展開</summary>

### よくある質問

#### Q: 左右で水の流れる量に差があるのは正常ですか？
**A:** 左側には電動ポンプが設置されており、ここで水の「吸い込み」と「排出」を行い、水を循環させます。そのため、左側の方が水の動きや膨らみを強く感じられることがあります。

#### Q: 結束バンドはどう使うのですか？
**A:** ポンプを固定するために使います。ただし、なくても基本は固定されているので、使うかどうかは任意で大丈夫です。

#### Q: ポンプの取り外し方はどうしたらいいですか？
**A:** 下記動画を参照してください。

</details>"""

    # 各パターンを試して置換
    original_body = body
    for pattern in patterns_to_replace:
        body = body.replace(pattern, cooling_vest_with_questions)
        if body != original_body:
            print(f"パターンマッチ成功: {pattern[:50]}...")
            break
    
    return body

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    # 現在の記事内容を取得
    print("現在の記事内容を取得中...")
    article_data = get_current_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        print("記事の取得に失敗しました")
        return
    
    current_body = article_data['body']
    
    print("冷却ベストの質問を追加中...")
    
    # 冷却ベストの質問を追加
    updated_body = add_cooling_vest_questions(current_body)
    
    # 変更があったかチェック
    if updated_body == current_body:
        print("⚠️ 冷却ベストセクションが見つからないか、既に質問が追加されています")
        return
    
    # 記事を更新
    success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
    
    if success:
        print("\n🎉 冷却ベストの質問追加が完了しました！")
        print("📝 追加された質問:")
        print("1. 左右で水の流れる量に差があるのは正常ですか？")
        print("2. 結束バンドはどう使うのですか？")
        print("3. ポンプの取り外し方はどうしたらいいですか？")
    else:
        print("\n❌ 質問の追加に失敗しました")

if __name__ == "__main__":
    main()