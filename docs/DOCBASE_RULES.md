# Docbase処理ルール

## 概要
このドキュメントは、Docbase APIを使用した記事の更新処理に関するルールとガイドラインをまとめたものです。

## 🔒 統一設定ルール（重要）

### 記事の公開範囲設定
**すべてのDocbase記事は「従業員のみ（G.O / 加島）」の公開範囲で作成・更新してください。**

- **設定値**: `"scope": "private"`
- **対象**: 新規作成・既存記事更新の両方
- **理由**: 機密情報やシステム詳細を含むため、社内限定とする

## ファイル構成
- `/Users/g.ohorudingusu/Docbase/` - Docbase関連のすべてのファイルを格納
  - `docbase_env/` - Python仮想環境
  - `docbase_helper.py` - 汎用的な記事操作スクリプト（新）
  - `docbase_helper.sh` - ワンコマンド実行用ヘルパー（新）
  - `setup_docbase_env.sh` - 環境自動セットアップスクリプト（新）
  - `docbase_updater.py` - メインの更新処理スクリプト
  - `update_docbase_article.py` - 個別記事更新用スクリプト
  - `update_docbase.sh` - 更新処理の実行シェルスクリプト

## 環境設定

### 初回セットアップ
```bash
# 1. .envファイルを作成
cp /Users/g.ohorudingusu/Docbase/.env.example /Users/g.ohorudingusu/Docbase/.env

# 2. .envファイルを編集して以下の値を設定
#    DOCBASE_API_TOKEN=your_api_token_here
#    DOCBASE_TEAM=your_team_name_here
#    DOCBASE_ARTICLE_ID=your_article_id_here
```

### 必要な環境変数
```bash
DOCBASE_API_TOKEN    # DocbaseのAPIトークン
DOCBASE_TEAM         # Docbaseのチーム名
DOCBASE_ARTICLE_ID   # 更新対象の記事ID
```

### 仮想環境の有効化
```bash
source /Users/g.ohorudingusu/Docbase/docbase_env/bin/activate
```

### 依存関係
- python-dotenv: .envファイルから環境変数を読み込む
- requests: Docbase APIとの通信

## 基本的な使用方法

### 🚀 新しい簡単な方法（推奨）

```bash
# 記事を取得
./docbase_helper.sh get 664151

# 記事にセクションを追加
./docbase_helper.sh add-section 664151 "充電仕様" "10.8V/2A"

# 記事の内容を更新
./docbase_helper.sh update 664151 new_content.md

# 記事一覧を表示
./docbase_helper.sh list

# クイック追加（対話形式）
./docbase_helper.sh quick-add 664151
```

**メリット:**
- 仮想環境の自動有効化
- 環境変数の自動読み込み
- エラーハンドリングの改善
- Windows改行コード（\r\n）の自動処理

### 従来の方法

#### 1. 記事の更新
```bash
cd /Users/g.ohorudingusu/Docbase
./update_docbase.sh
```

#### 2. スクリプトの直接実行
```bash
# 仮想環境を有効化してから
source docbase_env/bin/activate
python docbase_updater.py
# または
python update_docbase_article.py
```

## 処理フロー

1. **環境変数の確認**
   - 必要な環境変数がすべて設定されているか確認
   - 不足している場合はエラーメッセージを表示

2. **APIトークンの検証**
   - Docbase APIへの接続確認
   - 権限の確認

3. **記事の取得**
   - 指定された記事IDの記事を取得
   - 現在の内容を確認

4. **更新処理**
   - 新しい内容で記事を更新
   - レスポンスの確認

5. **エラーハンドリング**
   - API呼び出しエラー
   - ネットワークエラー
   - 権限エラー

## トラブルシューティング

### よくあるエラーと対処法

1. **ModuleNotFoundError**
   - 仮想環境が有効化されていない
   - 解決方法: `source docbase_env/bin/activate`を実行

2. **環境変数エラー**
   - 必要な環境変数が設定されていない
   - 解決方法: `.env`ファイルを確認、または環境変数を設定

3. **APIトークンエラー**
   - トークンが無効または期限切れ
   - 解決方法: Docbaseの設定画面から新しいトークンを発行

4. **記事IDエラー**
   - 指定した記事IDが存在しない
   - 解決方法: Docbaseで正しい記事IDを確認

## セキュリティ注意事項

- APIトークンは絶対にコードに直接記載しない
- `.env`ファイルは`.gitignore`に追加する
- トークンは定期的に更新する

## 開発時の注意点

1. **コード変更時**
   - 仮想環境内で作業する
   - 変更前にバックアップを取る

2. **新機能追加時**
   - このドキュメントも更新する
   - エラーハンドリングを適切に実装する

3. **デバッグ時**
   - ログ出力を活用する
   - API呼び出しの頻度に注意（レート制限）

## コンテンツ作成ルール

### 絵文字の使用について
**Docbaseについての作業では絵文字は不要です。**

- **記事タイトル**: 絵文字なしでシンプルに記載
- **セクション見出し**: 絵文字なしで明確な見出しを使用
- **理由**: Docbaseの記事は業務文書であり、プロフェッショナルな表現を維持するため

**例：**
- ❌ `## 🔌 PowerArQ について`
- ✅ `## PowerArQ について`

## 参考リンク
- [Docbase API ドキュメント](https://help.docbase.io/posts/45703)
- [Python requests ライブラリ](https://docs.python-requests.org/)

## 作業ログ

### 2025/7/24 - 記事707448の大規模再構成

#### 実施内容
1. **テーブル形式からdetails形式への変換**
   - 338行のテーブルデータから297個のFAQを抽出
   - 各FAQにWeb反映対象チェックボックスを追加

2. **セクション構造の再編成**
   - PowerArQシリーズ全般セクションを作成（42個のFAQ）
   - 各商品別セクションを独立作成：
     - PowerArQ1 について（1個）
     - PowerArQ 2 について（10個）
     - PowerArQ3について（14個）
     - PowerArQ Proについて（12個）
     - PowerArQ mini について（11個）
     - PowerArQ mini 2について（14個）
     - PowerArQ S7について（6個）
     - PowerArQ Maxについて（5個）
     - PowerArQ S10 Proについて（適切に配置）
   - PowerArQ Solar（ソーラーパネル）についてを独立（47個）
   - 電気一般に関する質問（135個）

3. **表示問題の修正**
   - セクション名の絵文字重複を修正
   - エスケープ文字の修正

4. **欠落情報の追加（6個のFAQ追加）**
   - PowerArQ 全シリーズ　シガーソケットの出力最大電力
   - PowerArQ 全シリーズ　ファンの動作条件
   - PowerArQ 全シリーズ　出力のW数の表示
   - PowerArQ 全シリーズ　自動で出力が停止する条件
   - 各PowerArQシリーズ　ACアダプターのランプの色

#### 最終結果
- FAQ総数: 303個（元データ306個から適切にクリーニング）
- セクション数: 11個
- 文字数: 約51,000文字

#### 使用スクリプト
- `restructure_powerarq_properly.py` - メイン変換処理
- `fix_display_issues.py` - 表示問題修正
- `add_missing_series_tables.py` - 欠落情報追加