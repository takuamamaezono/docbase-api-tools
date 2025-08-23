#!/usr/bin/env python3
"""
Asana-Docbase連携拡張機能のマニュアルをDocbaseに更新するスクリプト
"""
import os
import json
import requests
from datetime import datetime

# 環境変数から設定を読み込み
API_TOKEN = "docbase_25Nx-5dwQuuqMcwz3ycgdEwNTzECPxxuh7Ry5jrbfH6MC5gxYj2uxakyDGeaYP2X"
TEAM_NAME = "go"
ARTICLE_ID = "2705590"  # PowerArQ製品別FAQ記事ID（仮）

def read_manual_content():
    """DOCBASE_MANUAL.mdの内容を読み込む"""
    manual_path = "/Users/g.ohorudingusu/asana-docbase-extension/DOCBASE_MANUAL.md"
    
    try:
        with open(manual_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"マニュアルファイルが見つかりません: {manual_path}")
        return None

def get_current_article():
    """現在の記事内容を取得"""
    url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{ARTICLE_ID}"
    headers = {
        'X-DocBaseToken': API_TOKEN,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"記事の取得に失敗しました: {e}")
        return None

def update_article_with_manual():
    """記事にマニュアル内容を追記"""
    print("📖 DOCBASE_MANUAL.mdを読み込み中...")
    manual_content = read_manual_content()
    if not manual_content:
        return False
    
    print("📄 現在の記事を取得中...")
    current_article = get_current_article()
    if not current_article:
        return False
    
    current_body = current_article.get('body', '')
    
    # v2.5の更新情報を追記
    today = datetime.now().strftime('%Y年%m月%d日')
    update_content = f"""

---

## 🔗 Asana-Docbase連携拡張機能 マニュアル更新（v2.5）

*更新日: {today}*

### 📝 v2.5の新機能

#### ⚙️ ユーザー別設定機能
- Chrome拡張機能のオプションページから簡単設定
- 各ユーザーが独自のDocbase記事を設定可能
- Chrome Storage APIを使用してユーザーごとに設定を保存

#### 📝 セクション選択の柔軟化
- セクション選択を必須から任意に変更
- 「記事の最後に追記」オプションを追加
- セクションがない記事でも追記可能に

#### 🎨 UI/UXの改善
- ポップアップに大きな設定ボタンを追加
- 未設定時の警告表示
- 設定状態によってボタンの色が変化（赤→水色）

### 🚀 アップデート手順

1. **拡張機能の更新**
   - Chrome拡張機能ページで一度削除
   - v2.5を再度読み込み

2. **設定の確認**
   - 拡張機能アイコンをクリック
   - 「設定を開く」から記事設定を確認

### 📋 主な変更点

**セクション選択の新機能:**
- セクションを選択しない（記事の最後に追記）
- 「📝 記事の最後に追記」を選択
- 特定のセクションを選択

これにより、セクション構造に関係なく、どの記事にも追記可能になりました。

---

*詳細なマニュアルは拡張機能パッケージ内の `DOCBASE_MANUAL.md` をご確認ください。*

"""
    
    new_body = current_body + update_content
    
    # 記事を更新
    url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{ARTICLE_ID}"
    headers = {
        'X-DocBaseToken': API_TOKEN,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'body': new_body,
        'notice': False  # 更新通知をしない
    }
    
    try:
        print("🔄 記事を更新中...")
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
        
        print("✅ 記事の更新が完了しました!")
        print(f"📍 記事URL: https://{TEAM_NAME}.docbase.io/posts/{ARTICLE_ID}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 記事の更新に失敗しました: {e}")
        return False

if __name__ == "__main__":
    print("🔗 Asana-Docbase連携拡張機能マニュアル更新スクリプト")
    print("=" * 60)
    
    success = update_article_with_manual()
    
    if success:
        print("\n🎉 マニュアルの更新が完了しました!")
    else:
        print("\n❌ マニュアルの更新に失敗しました。")