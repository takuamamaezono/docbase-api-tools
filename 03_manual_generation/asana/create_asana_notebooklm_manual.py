#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

def create_docbase_article():
    """Docbaseに新規記事を作成する"""
    
    # 環境変数の取得
    api_token = os.getenv('DOCBASE_ACCESS_TOKEN')
    team_name = os.getenv('DOCBASE_TEAM')
    
    if not api_token or not team_name:
        print("エラー: 必要な環境変数が設定されていません")
        print("DOCBASE_ACCESS_TOKEN と DOCBASE_TEAM を .env ファイルに設定してください")
        return False

    # 記事の内容
    article_content = """# Asana-NotebookLM連携拡張機能 使用マニュアル

## 概要
AsanaのコメントやタスクからテキストをワンクリックでGoogle Docsに追記し、NotebookLMのナレッジベースとして活用するChrome拡張機能です。

## 🎯 主要機能
- ✅ Asanaテキストの選択・抽出
- ✅ Google Docsへの自動追記（Markdown形式）
- ✅ Q&A形式での情報整理
- ✅ NotebookLMとの自動連携
- ✅ チーム設定共有機能

---

## 📋 事前準備

### 1. Google Cloud Console設定（管理者のみ）
拡張機能を利用するには、Google Cloud Consoleでの設定が必要です。

<details>
<summary>🔧 Google Cloud Console設定手順（クリックで展開）</summary>

#### ステップ1: プロジェクト作成
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 「プロジェクトを選択」→「新しいプロジェクト」
3. プロジェクト名: `asana-notebooklm-extension`
4. 「作成」をクリック

#### ステップ2: API有効化
1. 作成したプロジェクトを選択
2. 「APIとサービス」→「ライブラリ」
3. 以下のAPIを検索して有効化：
   - **Google Docs API**
   - **Google Drive API**

#### ステップ3: OAuth 2.0設定
1. 「APIとサービス」→「OAuth同意画面」
2. User Type: 「外部」を選択
3. アプリ名: `Asana-NotebookLM連携`
4. テストユーザーに利用予定のGmailアドレスを追加

#### ステップ4: 認証情報作成
1. 「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「OAuth クライアント ID」
3. アプリケーションの種類: **「Chrome 拡張機能」**
4. アプリケーション ID: 拡張機能インストール後に表示されるID
5. 作成されたクライアントIDをメモ

</details>

### 2. Chrome拡張機能のインストール
1. 拡張機能ファイルをダウンロード
2. `chrome://extensions/` を開く
3. 「デベロッパーモード」をON
4. 「パッケージ化されていない拡張機能を読み込む」
5. フォルダを選択してインストール

---

## 🚀 初回セットアップ

### 管理者（初回設定者）

#### 1. 認証設定
1. **拡張機能アイコン**をクリック
2. **「Google認証をテスト」**をクリック
3. Googleアカウントでログイン・権限許可

#### 2. Google Docs準備
1. **新しいGoogle Docs**を作成
2. ファイル名を設定（例：「Asana-NotebookLM連携ドキュメント」）
3. **共有設定**を変更：
   - 右上「共有」→「リンクを知っている全員」
   - 権限：「編集者」
4. **ファイルIDを取得**：
   - URL: `https://docs.google.com/document/d/[ファイルID]/edit`
   - `/d/` と `/edit` の間の文字列がファイルID

#### 3. 拡張機能設定
1. 拡張機能ポップアップでファイルIDを入力
2. **「設定を保存」**をクリック
3. **「設定をエクスポート」**でJSONファイルをダウンロード
4. チームメンバーにJSONファイルを配布

#### 4. NotebookLM設定
1. [NotebookLM](https://notebooklm.google.com/) を開く
2. 「新しいノートブック」を作成
3. 「ソースを追加」→「Google Drive」
4. 作成したGoogle Docsファイルを選択

---

## 👥 チームメンバーのセットアップ

### 1. 拡張機能インストール
- 上記「Chrome拡張機能のインストール」と同じ手順

### 2. 設定インポート
1. **拡張機能アイコン**をクリック
2. **「設定をインポート」**をクリック
3. 管理者から受け取った**JSONファイル**を選択
4. 「設定をインポートしました」メッセージを確認

### 3. 個人認証
1. **「Google認証をテスト」**をクリック
2. 自分のGoogleアカウントでログイン・権限許可
3. 「Google認証成功！」メッセージを確認

---

## 📝 使用方法

### 日常利用の流れ

#### 1. Asanaでテキスト選択
1. **Asana**のタスク・コメント画面を開く
2. 追記したい**テキストを選択**
3. 右上に表示される**「NotebookLMに追記」**ボタンをクリック

#### 2. 内容入力
モーダルダイアログが表示されるので：
1. **タイトル**を入力（例：「プロジェクトA 進捗確認」）
2. **質問内容**を入力（例：「現在の進捗状況は？」）
3. **回答内容**を入力（例：「80%完了、来週リリース予定」）

#### 3. 追記実行
1. **「NotebookLMに追記」**ボタンをクリック
2. 「追記が完了しました」メッセージを確認
3. Google Docsに自動で内容が追記される

#### 4. NotebookLMで確認
- NotebookLMが自動でファイル変更を検知
- 新しい情報がすぐに利用可能になる

---

## 🔧 トラブルシューティング

### よくある問題と解決方法

<details>
<summary>❌ 「エラー 400: invalid_request」が表示される</summary>

**原因**: OAuth設定の問題

**解決方法**:
1. Google Cloud ConsoleでOAuth同意画面を確認
2. テストユーザーに自分のGmailアドレスが追加されているか確認
3. **Google Chrome**ブラウザを使用（他のブラウザは非対応）

</details>

<details>
<summary>❌ 「Google Docs API エラー: 403」が表示される</summary>

**原因**: API権限またはファイルアクセス権限の問題

**解決方法**:
1. Google DocsファイルIDが正しいか確認
2. ファイル共有設定を「リンクを知っている全員が編集可能」に変更
3. Google Cloud ConsoleでGoogle Docs APIが有効化されているか確認

</details>

<details>
<summary>❌ 「NotebookLMに追記」ボタンが表示されない</summary>

**原因**: 拡張機能の読み込み問題

**解決方法**:
1. `chrome://extensions/` で拡張機能をリロード
2. Asanaページを再読み込み
3. デベロッパーツール（F12）でConsoleエラーを確認

</details>

<details>
<summary>❌ 設定インポートが失敗する</summary>

**原因**: JSONファイルの形式問題

**解決方法**:
1. 正しい設定ファイル（拡張機能でエクスポートしたもの）を使用
2. ファイルが破損していないか確認
3. 手動でファイルIDを入力して設定保存

</details>

---

## 📊 活用のコツ

### 効果的な使い方

#### 1. 定期的な情報蓄積
- **毎日の進捗報告**をAsanaからNotebookLMに蓄積
- **問題・解決策**をQ&A形式で整理
- **決定事項・議事録**の要点を追記

#### 2. 検索しやすい形式で記録
- **具体的なタイトル**を付ける
- **キーワード**を含める
- **日付・プロジェクト名**を明記

#### 3. チーム知識の共有
- 同じGoogle Docsファイルに全員で追記
- NotebookLMで過去の情報を素早く検索
- 新メンバーのオンボーディングに活用

---

## 📋 仕様・制限事項

### 技術仕様
- **対応ブラウザ**: Google Chrome（推奨）
- **認証方式**: OAuth 2.0（個人認証）
- **出力形式**: Markdown形式
- **API**: Google Docs API v1, Google Drive API

### 制限事項
- 各メンバーが個別にGoogle認証が必要
- NotebookLMへのソース追加は手動（初回のみ）
- Google Chromeブラウザでの利用を推奨

### セキュリティ
- OAuthによる安全な認証
- APIトークンは拡張機能内で安全に管理
- Google Docsファイルの共有権限で利用者を制御

---

## 🎯 期待される効果

### 個人レベル
- ✅ Asanaでの作業内容を簡単にナレッジ化
- ✅ 過去の経験・知見を素早く検索
- ✅ 手作業でのコピペ作業を削減

### チームレベル
- ✅ 属人化した知識の共有
- ✅ プロジェクトノウハウの蓄積
- ✅ 新メンバーの学習促進

### 組織レベル
- ✅ 組織知識の体系化
- ✅ 意思決定の透明性向上
- ✅ 業務効率の大幅改善

---

## 📞 サポート

### 困ったときは
1. **このマニュアル**のトラブルシューティングを確認
2. **開発ログ.md**で詳細な技術情報を確認
3. **管理者**に相談

### 改善要望
- 新機能のリクエスト
- 不具合の報告
- 使い勝手の改善提案

---

*最終更新: 2024年7月24日*
*作成者: Claude AI*"""

    # APIリクエストのデータ
    data = {
        "title": "Asana-NotebookLM連携拡張機能 使用マニュアル",
        "body": article_content,
        "draft": False,  # 公開状態で作成
        "notice": True,   # 通知を送信
        "tags": [
            {"name": "Asana"},
            {"name": "NotebookLM"},
            {"name": "Chrome拡張機能"},
            {"name": "マニュアル"},
            {"name": "Google Docs"},
            {"name": "ナレッジベース"}
        ]
    }

    # APIエンドポイント
    url = f"https://api.docbase.io/teams/{team_name}/posts"
    
    # リクエストヘッダー
    headers = {
        "X-DocBaseToken": api_token,
        "Content-Type": "application/json"
    }

    try:
        print("Docbaseに記事を作成中...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ 記事が正常に作成されました")
            print(f"📄 記事ID: {result['id']}")
            print(f"🔗 URL: {result['url']}")
            return True
        else:
            print(f"❌ エラーが発生しました: {response.status_code}")
            print(f"レスポンス: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 例外エラー: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Asana-NotebookLM連携拡張機能マニュアルをDocbaseに作成します")
    success = create_docbase_article()
    
    if success:
        print("\n🎉 マニュアルの作成が完了しました！")
    else:
        print("\n❌ マニュアルの作成に失敗しました。")
        print("環境変数の設定を確認してください。")