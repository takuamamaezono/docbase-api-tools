# Docbase管理システム

Docbase記事の管理・更新・自動化ツールのコレクションです。

## 📁 フォルダ構造

### 🔧 01_docbase_core/ - コア機能
Docbaseの基本的な記事更新機能

- `docbase_helper.py` - 汎用記事操作ヘルパー
- `docbase_updater.py` - メイン記事更新スクリプト
- `update_docbase_article.py` - 個別記事更新
- `update_docbase.sh` - 実行用シェルスクリプト
- `create_docbase_article.py` - 新規記事作成

**使い方:**
```bash
cd 01_docbase_core
./update_docbase.sh
```

### ❓ 02_faq_management/ - FAQ管理システム
FAQ記事の管理・更新・分析ツール

#### add_flags/ - フラグ追加機能
- FAQ項目にWeb反映フラグを追加

#### analyze/ - 分析機能
- FAQ内容の分析・比較・確認ツール

#### update/ - 更新・修正機能
- FAQの構造変更・修正・再編成

**メイン機能:**
- `faq_flag_manager.py` - フラグ管理
- `FAQ_FLAG_GUIDE.md` - フラグ機能ガイド

### 📚 03_manual_generation/ - マニュアル作成システム
各種マニュアル・記事の自動生成

#### asana/ - Asana関連
- Asana拡張機能のマニュアル作成

#### beginner/ - 初心者向け
- 初心者向けマニュアルの作成

#### chatbot/ - チャットボット用
- チャットボット向けコンテンツ作成

### 🤖 04_article_automation/ - 記事自動化システム
記事の自動化関連機能

#### old_article_warning/ - 古い記事警告システム
- 古い記事に警告を追加するシステム
- `README.md` - 詳細な使用方法

#### その他の自動化機能
- `create_shopify_folder_structure_article.py` - Shopify記事自動生成

### 🛠️ 05_work_scripts/ - 作業用スクリプト
個別の作業・更新用スクリプト集

- 特定記事の更新・取得スクリプト
- セクション移動・追加スクリプト
- 一時的な作業用ツール

### 📖 docs/ - ドキュメント
システムのルールとAPIガイド

- `DOCBASE_API_GUIDE.md` - API使用方法
- `POWERARQ_FAQ_AUTOMATION_LOG.md` - プロジェクトログ

### 🗄️ archive/ - アーカイブ
使用頻度の低いファイル・履歴保存

### 🔧 ルートヘルパースクリプト
プロジェクト全体を管理する共通ツール

- `docbase_dev_helper.sh` - メイン開発ヘルパー（記事操作）
- `docbase_tag_helper.sh` - タグ管理専用ヘルパー
- `setup_docbase_env.sh` - 環境セットアップスクリプト

## 🚀 よく使うコマンド

### 基本的な記事更新
```bash
cd 01_docbase_core
./update_docbase.sh
```

### FAQ管理
```bash
cd 02_faq_management
python faq_flag_manager.py
```

### 開発ヘルパー（ルートから実行）
```bash
# メイン開発ヘルパー
./docbase_dev_helper.sh get <記事ID>        # 記事取得
./docbase_dev_helper.sh update <記事ID> <ファイル>  # 記事更新
./docbase_dev_helper.sh add-section <記事ID> <セクション名> <内容>  # セクション追加

# タグ管理ヘルパー
./docbase_tag_helper.sh tags               # 既存タグ一覧表示
./docbase_tag_helper.sh create <タイトル> <ファイル>  # インタラクティブタグ選択で記事作成
```

## ⚙️ 環境設定

### 初回セットアップ
```bash
# 環境セットアップスクリプトを実行
./setup_docbase_env.sh

# 仮想環境を有効化
source docbase_env/bin/activate

# 環境変数を設定（.envファイル）
DOCBASE_API_TOKEN=your_token
DOCBASE_TEAM=your_team
DOCBASE_ARTICLE_ID=your_article_id
```

## 🔒 重要な注意事項

1. **公開範囲**: すべての記事は「従業員のみ」で作成
2. **APIトークン**: 絶対にコードに直接記載しない
3. **バックアップ**: 重要な更新前はバックアップを取る

## 📞 サポート

- ルール確認: `docs/DOCBASE_RULES.md`
- API情報: `docs/DOCBASE_API_GUIDE.md`
- 問題があれば: 各フォルダのREADME.mdを確認

---

最終更新: 2025年1月31日