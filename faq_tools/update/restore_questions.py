#!/usr/bin/env python3
"""
削除された質問を復元するスクリプト
"""

import requests
import json
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

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

def restore_point_cooler_questions(body):
    """
    ポイントクーラーの質問を復元
    """
    # 現在の空のポイントクーラーセクションを探す
    point_cooler_empty = """## ❄️ ポイントクーラー

<details>
<summary>クリックして展開</summary>


---
 
よくある質問

現在、特定の質問は記載されていません。

</details>"""

    # 復元する質問内容
    point_cooler_restored = """## ❄️ ポイントクーラー

<details>
<summary>クリックして展開</summary>

### よくある質問

#### Q: ポイントクーラーとは何ですか？
**A:** ポイントクーラーは、特定の場所を効率的に冷却するための装置です。

#### Q: どのような条件で消費電力が高くなりますか？
**A:** 周囲の気温や湿度が高い場合、冷却の負荷が大きくなり、消費電力が上がります。特に高温多湿の環境では、最大200W程度に達する場合があります。

#### Q: 消費電力が急に下がることがあるのはなぜですか？
**A:** インバーター式のため、設定温度に達するとコンプレッサーの運転が自動的に停止し、消費電力が大きく下がります（例：150Wから9W程度まで）。再び冷却が必要になると、コンプレッサーが作動し消費電力が上がります。

#### Q: インバーター式とは何ですか？
**A:** インバーター式は、冷却の必要に応じてコンプレッサーの運転を自動調整する方式です。これにより、効率的に温度を管理し、無駄な消費電力を抑えることができます。

#### Q: スリープモードとは何ですか？
**A:** 本来音をOFFにするための機能なのですが、本製品は開発の中で最初から音を切ることにしたため、本製品でこのモードを使用する必要はありません

#### Q: 説明書に記載はないですが、DCの入力は可能ですか？
**A:** はい、可能です。DC入力の規格としては「DC24V／MAX10A、最大出力は200W」になります。

#### Q: 冷却方式は何ですか？
**A:** コンプレッサー式になります。

#### Q: アルコールで本体を拭いてもいいですか？
**A:** アルコールありのウェットティッシュで拭いても特に問題ありませんが、念の為、アルコールの液体を直接塗布するのは避けるようにしてください。

#### Q: 本体に油っぽいものがついていますが、どうしたら良いですか？
**A:** シール剥がしを利用して拭き取りを行っていただくようにご案内ください。

</details>"""

    # テストの質問も削除
    test_question = """---
*Asanaより追記 (2025/7/24)*
**Q: テスト**
**A: テスト・テスト**


"""

    # テスト質問を削除
    body = body.replace(test_question, "")
    
    # ポイントクーラーの質問を復元
    body = body.replace(point_cooler_empty, point_cooler_restored)
    
    return body

def main():
    TEAM_NAME = "go"
    POST_ID = 2705590
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    # バックアップファイルから現在の記事内容を読み込み
    try:
        with open('article_backup.json', 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        current_body = article_data['body']
    except FileNotFoundError:
        print("article_backup.jsonファイルが見つかりません")
        return
    
    print("削除された質問を復元中...")
    
    # ポイントクーラーの質問を復元
    updated_body = restore_point_cooler_questions(current_body)
    
    # 記事を更新
    success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
    
    if success:
        print("\n🎉 削除された質問の復元が完了しました！")
        print("📝 復元された内容:")
        print("- ポイントクーラーの9つの質問を復元")
        print("- テスト質問を削除")
    else:
        print("\n❌ 復元に失敗しました")

if __name__ == "__main__":
    main()