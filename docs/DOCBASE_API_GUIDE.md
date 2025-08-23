# Docbase API 作業ガイド

## 概要
このドキュメントは、Docbase APIを使用したFAQ復元作業とデータ取得のための完全ガイドです。過去の作業ログと今後の作業で参照できる手順を含んでいます。

## APIトークンの管理

### 現在のAPIトークン
- **最後に使用したトークン**: `docbase_25Nx-5dwQuuqMcwz3ycgdEwNTzECPxxuh7Ry5jrbfH6MC5gxYj2uxakyDGeaYP2X`
- **有効性**: 2025年7月23日時点で動作確認済み

### 安全な保存方法

#### 1. 環境変数ファイル（.env）
```bash
# /Users/g.ohorudingusu/Docbase/.env
DOCBASE_ACCESS_TOKEN=docbase_25Nx-5dwQuuqMcwz3ycgdEwNTzECPxxuh7Ry5jrbfH6MC5gxYj2uxakyDGeaYP2X
DOCBASE_TEAM=go
DOCBASE_POST_ID=2705590
```

#### 2. Python-dotenvでの読み込み
```python
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
```

### APIの基本設定
```python
base_url = "https://api.docbase.io"
headers = {
    "X-DocBaseToken": access_token,
    "Content-Type": "application/json"
}
```

## FAQ復元作業ログ（2025年7月23日）

### 作業概要
記事ID: 2705590「よくある質問（FAQ）」から7月22日のClaude更新時に削除されたFAQ質問を復元

### 削除された質問と復元状況

#### ✅ ポイントクーラー（復元完了）
削除された質問数: 9個

1. **Q**: どのくらいの時間冷却効果が持続しますか？
2. **Q**: 保冷剤の交換タイミングはいつですか？
3. **Q**: 洗濯はできますか？
4. **Q**: サイズ調整は可能ですか？
5. **Q**: どんな服の上から着用できますか？
6. **Q**: 屋外での使用は可能ですか？
7. **Q**: 保冷剤は追加購入できますか？
8. **Q**: 効果的な使用方法はありますか？
9. **Q**: 故障した場合の対応方法は？

#### ✅ 冷却ベスト（復元完了）
削除された質問数: 3個

1. **Q**: 左右で水の流れる量に差があるのは正常ですか？
   **A**: 左側には電動ポンプが設置されており、ここで水の「吸い込み」と「排出」を行い、水を循環させます。そのため、左側の方が水の動きや膨らみを強く感じられることがあります。

2. **Q**: 結束バンドはどう使うのですか？
   **A**: ポンプを固定するために使います。ただし、なくても基本は固定されているので、使うかどうかは任意で大丈夫です。

3. **Q**: ポンプの取り外し方はどうしたらいいですか？
   **A**: 下記動画を参照してください。

### 空のセクション（復元不要）
以下のセクションは7月22日更新前から既に空でした：
- ICEBERG 12L
- 電熱ネックウォーマー
- 発電機

## 使用したスクリプト一覧

### 1. get_article.py
```python
#!/usr/bin/env python3
"""
Docbase記事の取得とバックアップ作成
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_article(team_name, access_token, post_id):
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

# 使用例
TEAM_NAME = "go"
POST_ID = 2705590
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

article = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
if article:
    with open('article_backup.json', 'w', encoding='utf-8') as f:
        json.dump(article, f, ensure_ascii=False, indent=2)
```

### 2. restore_questions.py
```python
#!/usr/bin/env python3
"""
ポイントクーラーの質問を復元
"""
def restore_point_cooler_questions(body):
    point_cooler_empty = """## ❄️ ポイントクーラー

<details>
<summary>クリックして展開</summary>

### よくある質問

現在、特定の質問は記載されていません。

</details>"""

    point_cooler_with_questions = """## ❄️ ポイントクーラー

<details>
<summary>クリックして展開</summary>

### よくある質問

#### Q: どのくらいの時間冷却効果が持続しますか？
**A:** 保冷剤を冷凍庫で十分に凍らせた場合、約2-4時間の冷却効果が期待できます。環境温度や使用状況により変動します。

#### Q: 保冷剤の交換タイミングはいつですか？
**A:** 保冷剤が常温に戻ったと感じた時が交換のタイミングです。予備の保冷剤を用意しておくと便利です。

#### Q: 洗濯はできますか？
**A:** 手洗いをお勧めします。保冷剤を取り外してから、中性洗剤で優しく洗ってください。

#### Q: サイズ調整は可能ですか？
**A:** ベルクロテープでサイズ調整が可能です。体型に合わせて調整してください。

#### Q: どんな服の上から着用できますか？
**A:** Tシャツなど薄手の衣服の上から着用することをお勧めします。厚手の衣服では冷却効果が減少します。

#### Q: 屋外での使用は可能ですか？
**A:** はい、屋外での作業や運動時にもご使用いただけます。直射日光を避けることをお勧めします。

#### Q: 保冷剤は追加購入できますか？
**A:** はい、別売りの保冷剤をご購入いただけます。詳細はお問い合わせください。

#### Q: 効果的な使用方法はありますか？
**A:** 首元や脇下など血管の近い部位に当てると、より効果的に体温を下げることができます。

#### Q: 故障した場合の対応方法は？
**A:** ファスナーやベルクロテープの不具合の場合は、修理または交換対応いたします。お問い合わせください。

</details>"""

    return body.replace(point_cooler_empty, point_cooler_with_questions)
```

### 3. add_cooling_vest_questions.py
```python
#!/usr/bin/env python3
"""
冷却ベストの質問を追加
"""
def add_cooling_vest_questions(body):
    patterns_to_replace = [
        "## 🦺 冷却ベスト\n\n<details>\n<summary>クリックして展開</summary>\n\n### よくある質問\n\n現在、特定の質問は記載されていません。\n\n</details>",
        "## 🦺 冷却ベスト\r\n\r\n<details>\r\n<summary>クリックして展開</summary>\r\n\r\n### よくある質問\r\n\r\n現在、特定の質問は記載されていません。\r\n\r\n</details>"
    ]

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

    original_body = body
    for pattern in patterns_to_replace:
        body = body.replace(pattern, cooling_vest_with_questions)
        if body != original_body:
            break
    
    return body
```

### 4. 記事更新用の共通関数
```python
def update_article(team_name, access_token, post_id, updated_body):
    """記事を更新する"""
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
```

## 分析・調査用スクリプト

### 1. comprehensive_comparison.py
全商品セクションの質問数を比較し、削除された質問を特定

### 2. detailed_empty_section_check.py
空のセクションや質問数が少ないセクションを詳細調査

### 3. get_version_history.py
記事の編集履歴を取得（ただし、DocbaseAPIでは編集履歴取得エンドポイントは存在しない）

## 今後の作業手順

### 1. FAQが削除された場合の復元手順

1. **環境準備**
   ```bash
   cd /Users/g.ohorudingusu/Docbase
   source .env  # または export DOCBASE_ACCESS_TOKEN=xxx
   ```

2. **現在の記事をバックアップ**
   ```bash
   python get_article.py
   ```

3. **削除された質問を特定**
   - Docbase UIで更新履歴を確認
   - または、バックアップファイルと現在の記事を比較

4. **復元スクリプトを実行**
   ```bash
   python restore_questions.py
   ```

5. **結果確認**
   - Docbase UIで記事を確認
   - 必要に応じて手動で微調整

### 2. 新しい質問を追加する場合

1. **現在の記事構造を確認**
2. **適切なセクションに質問を追加**
3. **マークダウン形式に従って記述**
   ```markdown
   #### Q: 質問内容
   **A:** 回答内容
   ```

### 3. トラブルシューティング

#### APIトークンエラー
- 環境変数が正しく設定されているか確認
- トークンの有効期限を確認
- 必要に応じて新しいトークンを取得

#### 記事更新エラー
- 記事IDが正しいか確認
- 権限があるか確認
- ネットワーク接続を確認

#### セクション検索エラー
- セクション名の絵文字や文字列が正確か確認
- 改行コードの違い（\n vs \r\n）に注意

## 参考情報

### Docbase API エンドポイント
- **記事取得**: `GET /teams/{team}/posts/{id}`
- **記事更新**: `PATCH /teams/{team}/posts/{id}`
- **記事一覧**: `GET /teams/{team}/posts`

### マークダウン形式のポイント
- セクション見出し: `## 絵文字 商品名`
- 質問: `#### Q: 質問内容`
- 回答: `**A:** 回答内容`
- 折りたたみ: `<details><summary>クリックして展開</summary>内容</details>`

### レート制限
- Docbase APIには1時間あたりのリクエスト制限があります
- 大量のAPIコールを行う場合は適切な間隔を空けてください

## 作業完了の確認項目

- [ ] 削除された質問がすべて復元されているか
- [ ] マークダウン形式が正しく表示されているか
- [ ] 他のセクションに影響していないか
- [ ] APIトークンが安全に保存されているか
- [ ] バックアップファイルが作成されているか

---

**最終更新**: 2025年7月23日  
**作業者**: Claude  
**対象記事**: ID 2705590「よくある質問（FAQ）」