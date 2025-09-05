#!/usr/bin/env python3
"""
Asana-Docbase連携拡張機能の初心者向けマニュアルをDocbaseに投稿するスクリプト
"""
import os
import json
import requests
from datetime import datetime

# 環境変数から設定を読み込み
API_TOKEN = "docbase_25Nx-5dwQuuqMcwz3ycgdEwNTzECPxxuh7Ry5jrbfH6MC5gxYj2uxakyDGeaYP2X"
TEAM_NAME = "go"
ARTICLE_ID = "3873863"

def create_manual_content():
    """初心者向けマニュアルの内容を作成"""
    today = datetime.now().strftime('%Y年%m月%d日')
    
    content = f"""# 🔗 Asana-Docbase連携拡張機能 かんたん導入ガイド

*最終更新: {today}*  
*バージョン: v2.5*

## 📌 この拡張機能でできること

**AsanaのコメントをワンクリックでDocbaseのFAQ記事に追記できます！**

例えば：
- お客様からの質問と回答をFAQに追加
- チーム内の有益な情報をDocbaseに蓄積
- 手動でコピペする手間を削減

## 🚀 10分でできる！導入手順

### ステップ1：拡張機能をダウンロード（2分）

1. **[📦 Google Driveを開く](https://drive.google.com/drive/u/0/folders/0AGGfrFoffWauUk9PVA)**
2. `asana-docbase-extension` フォルダを右クリック
3. **「ダウンロード」**を選択
   - 自動的にzipファイルとしてダウンロードされます
4. ダウンロードしたzipファイルを**ダブルクリック**して解凍
   - 📁 `asana-docbase-extension` フォルダが作成されます

### ステップ2：Chromeに拡張機能を追加（3分）

1. **Chromeブラウザ**を開く
2. アドレスバーに `chrome://extensions/` と入力してEnter
3. 右上の「**デベロッパーモード**」をONにする
   - ![デベロッパーモード](スイッチをONに)
4. 「**パッケージ化されていない拡張機能を読み込む**」をクリック
5. 先ほど解凍したフォルダを選択

✅ 「Asana-Docbase連携」が表示されたら成功！

### ステップ3：初期設定（5分）

#### 3-1. 拡張機能アイコンをクリック
- Chromeの右上に表示される拡張機能アイコン（パズルのピース）をクリック
- 「Asana-Docbase連携」をクリック

#### 3-2. 設定画面を開く
- 赤い「**初期設定を行う（必須）**」ボタンをクリック
- 設定画面が開きます

#### 3-3. 必要な情報を入力

**① Docbase APIトークン**
1. [Docbaseにログイン](https://go.docbase.io)
2. 右上のプロフィール → 「設定」
3. 「アプリケーション」タブ → 「新しいトークンを作成」
4. 名前：`Asana連携` / スコープ：`read`と`write`にチェック
5. 作成されたトークンをコピー

**② Docbaseチーム名**
- `go` と入力（URLの https://go.docbase.io の go 部分）

**③ 追記先の記事を追加**
1. 「新しい記事を追加」ボタンをクリック
2. 記事名：わかりやすい名前（例：PowerArQ FAQ）
3. 記事ID：DocbaseのURLの最後の数字
   - 例：`https://go.docbase.io/posts/2705590` → `2705590`

#### 3-4. 設定を保存
「**設定を保存**」ボタンをクリック → 完了！🎉

## 📝 使い方（超かんたん！）

### 基本の使い方

1. **Asanaでタスクを開く**
2. **コメントのテキストを選択**
3. **画面下のボタンをクリック**：
   - 💙 **質問を挿入**：選択したテキストを質問として
   - 💚 **回答を挿入**：選択したテキストを回答として
   - 💛 **FAQ追記**：自由に入力
4. **記事を選択して「追記する」**

### 💡 便利な使い方

**ケース1：お客様からの質問と回答をFAQに**
1. 質問コメントを選択 → 「質問を挿入」
2. 回答コメントを選択 → 「回答を挿入」
3. 記事を選んで「追記する」

**ケース2：セクションがない記事でも大丈夫**
- セクション選択で「📝 記事の最後に追記」を選ぶだけ！

## ❓ よくある質問

### Q: ボタンが表示されません
**A:** 以下を確認してください：
1. `chrome://extensions/` で拡張機能が有効になってるか
2. Asanaのページを再読み込み（Ctrl+R）
3. サイトアクセス権限が許可されてるか

### Q: 「記事の取得に失敗しました」エラーが出ます
**A:** 記事の公開設定を確認：
- Docbaseで記事を開く
- 「自分だけ」→「グループに公開」または「全体に公開」に変更
- あなたがその記事を閲覧できることを確認

### Q: 新しく追加した記事が使えません
**A:** 以下を試してください：
1. 記事IDが数字のみか確認（スペースや文字が入ってないか）
2. Asanaページを再読み込み
3. 設定画面で記事を削除→再追加

## 🆘 困ったときは

### それでも解決しない場合

1. **拡張機能を一度削除して再インストール**
   - `chrome://extensions/` → 削除 → もう一度ステップ2から

2. **コンソールでエラーを確認**
   - AsanaページでF12 → Consoleタブ
   - 赤いエラーメッセージをコピー

3. **チームに相談**
   - エラーメッセージと一緒に技術チームに連絡

## 📊 動作確認済み環境

- Chrome バージョン 90以降
- Windows 10/11、macOS 10.15以降
- Asana（app.asana.com）
- Docbase（go.docbase.io）

## 🎯 次のステップ

導入が完了したら：
1. まずは1つ、簡単なFAQを追記してみましょう
2. チームメンバーにも共有してください
3. 使い方で分からないことがあれば遠慮なく質問を！

---

*このマニュアルは定期的に更新されます。*
"""
    
    return content

def update_article():
    """記事を更新"""
    content = create_manual_content()
    
    url = f"https://api.docbase.io/teams/{TEAM_NAME}/posts/{ARTICLE_ID}"
    headers = {
        'X-DocBaseToken': API_TOKEN,
        'Content-Type': 'application/json'
    }
    
    # まず現在の記事を取得
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        current_article = response.json()
    except Exception as e:
        print(f"❌ 記事の取得に失敗: {e}")
        return False
    
    # 記事を更新
    payload = {
        'title': current_article.get('title', 'Asana-Docbase連携拡張機能 かんたん導入ガイド'),
        'body': content,
        'notice': False
    }
    
    try:
        print("📝 記事を更新中...")
        response = requests.patch(url, headers=headers, json=payload)
        response.raise_for_status()
        
        print("✅ 記事の更新が完了しました!")
        print(f"📍 記事URL: https://{TEAM_NAME}.docbase.io/posts/{ARTICLE_ID}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 記事の更新に失敗しました: {e}")
        return False

if __name__ == "__main__":
    print("📝 初心者向けマニュアル作成スクリプト")
    print("=" * 60)
    
    success = update_article()
    
    if success:
        print("\n🎉 マニュアルの作成が完了しました!")
    else:
        print("\n❌ マニュアルの作成に失敗しました。")