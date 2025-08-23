#!/usr/bin/env python3
"""
DocBase記事に変更履歴を追加して更新するスクリプト
"""

import requests
import os
from datetime import datetime

# 設定
TEAM_NAME = "go"
POST_ID = 2705590
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    print("エラー: DOCBASE_ACCESS_TOKEN が設定されていません")
    exit(1)

# 変更履歴を作成
changelog = """

---

## 📝 更新履歴

### 2025年7月22日 更新
**更新者**: Claude Code  
**更新内容**: 記事全体の可読性向上のための大規模リフォーマット

#### 🔄 主な変更点

1. **📋 目次の追加**
   - 全21商品カテゴリーへのクイックアクセスリンクを追加
   - ページ内リンクで素早く目的の商品情報へジャンプ可能に

2. **🔗 関連リンクセクションの新設**
   - 全商品FAQ、注文番号関連、不具合チェックリストなどの重要リンクを集約
   - 記事冒頭に配置してアクセシビリティを向上

3. **📦 商品ごとの表示改善**
   - `<details>`タグを使用した折りたたみ可能な構造に変更
   - 長い内容でもページ全体がスッキリと見やすく
   - 必要な商品情報だけを展開して閲覧可能

4. **🎨 視覚的な改善**
   - 各商品カテゴリーに関連するアイコンを追加（❄️ 🧊 💨 🛏️ など）
   - 見出しレベルを適切に調整（H2、H3、H4）
   - Q&A形式を統一（#### Q: 質問 / **A:** 回答）

5. **📸 画像の説明追加**
   - すべての画像にalt属性的な説明を追加
   - 画像が何を示しているか分かりやすく

6. **📑 構造の整理**
   - 質問と回答を明確に区別
   - 重要な注意事項を⚠️マークで強調
   - コードブロックや引用を適切にフォーマット

#### 🔍 変更前後の比較

**変更前**: 
- 長い表形式で全商品のFAQが羅列
- スクロールが大変で目的の情報を見つけにくい
- 商品カテゴリーの区別が不明瞭

**変更後**:
- 目次から直接アクセス可能
- 折りたたみ式で必要な情報だけを表示
- アイコンとフォーマットで視覚的に整理

---
"""

# 現在の内容を取得
url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{POST_ID}"
headers = {
    "X-DocBaseToken": ACCESS_TOKEN,
    "Content-Type": "application/json"
}

print("現在の記事内容を取得中...")
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    current_content = response.json().get('body', '')
except requests.exceptions.RequestException as e:
    print(f"記事の取得に失敗しました: {e}")
    exit(1)

# フォーマット済みの内容を読み込む
print("フォーマット済みの内容を読み込んでいます...")
with open('formatted_post_content.md', 'r', encoding='utf-8') as f:
    formatted_content = f.read()

# 変更履歴を追加した新しい内容を作成
new_body = formatted_content + changelog

# 更新を実行
update_data = {
    "body": new_body
}

print(f"記事ID {POST_ID} を更新しています（変更履歴付き）...")
try:
    response = requests.patch(url, headers=headers, json=update_data)
    response.raise_for_status()
    print("✅ 記事の更新に成功しました！（変更履歴を追加）")
    print(f"更新日時: {response.json().get('updated_at', 'N/A')}")
    print(f"URL: https://go.docbase.io/posts/{POST_ID}")
except requests.exceptions.RequestException as e:
    print(f"❌ 記事の更新に失敗しました: {e}")
    if hasattr(e.response, 'text'):
        print(f"エラー詳細: {e.response.text}")