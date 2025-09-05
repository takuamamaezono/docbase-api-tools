#!/usr/bin/env python3
"""
冷却ベストの質問を追加する簡単なスクリプト
"""

import requests
import os
import re

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    # 記事を取得
    headers = {
        'X-DocBaseToken': ACCESS_TOKEN,
        'Content-Type': 'application/json'
    }
    
    url = f'https://api.docbase.io/teams/{TEAM_NAME}/posts/{POST_ID}'
    response = requests.get(url, headers=headers)
    article = response.json()
    body = article['body']
    
    # 冷却ベストセクションを見つけて置換
    # 正規表現で冷却ベストセクション全体をマッチ
    pattern = r'(## 🦺 冷却ベスト.*?</details>)'
    
    replacement = """## 🦺 冷却ベスト

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
    
    # 正規表現で置換（DOTALL フラグで改行もマッチ）
    updated_body = re.sub(pattern, replacement, body, flags=re.DOTALL)
    
    if updated_body == body:
        print("⚠️ 冷却ベストセクションが見つからないか、既に更新されています")
        # デバッグ用：冷却ベスト周辺を表示
        cooling_start = body.find('冷却ベスト')
        if cooling_start > -1:
            print("現在の冷却ベストセクション:")
            print(body[cooling_start-50:cooling_start+800])
        return
    
    # 記事を更新
    update_data = {"body": updated_body}
    response = requests.patch(url, headers=headers, json=update_data)
    
    if response.status_code == 200:
        print("✅ 冷却ベストの質問追加が完了しました！")
        print("📝 追加された質問:")
        print("1. 左右で水の流れる量に差があるのは正常ですか？")
        print("2. 結束バンドはどう使うのですか？")
        print("3. ポンプの取り外し方はどうしたらいいですか？")
    else:
        print(f"❌ 更新に失敗しました: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()