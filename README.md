# Docbase管理システム

Docbase記事の管理・更新・自動化ツールのコレクションです。

## 📁 フォルダ構造

### 🔧 core/ - コア機能
Docbaseの基本的な記事更新機能

- `docbase_env/` - Python仮想環境
- `docbase_updater.py` - メイン記事更新スクリプト
- `update_docbase_article.py` - 個別記事更新
- `update_docbase.sh` - 実行用シェルスクリプト

**使い方:**
```bash
cd core
./update_docbase.sh
```

### 📚 docs/ - ドキュメント
システムのルールとAPIガイド

- `DOCBASE_RULES.md` - 重要なルールと設定
- `DOCBASE_API_GUIDE.md` - API使用方法

### 📝 lp_generator/ - LP欄生成システム
商品のLP欄を自動生成するシステム（新機能）

**使い方:**
```bash
cd lp_generator
./run_lp_generator.sh
```

### 🔍 faq_tools/ - FAQ管理ツール
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

### 📖 manual_creators/ - マニュアル作成ツール
各種マニュアル・記事の自動生成

#### asana/ - Asana関連
- Asana拡張機能のマニュアル作成

#### beginner/ - 初心者向け
- 初心者向けマニュアルの作成

#### chatbot/ - チャットボット用
- チャットボット向けコンテンツ作成

### ⚠️ old_article_warning/ - 古い記事警告システム
古い記事に警告を追加するシステム

### 🗄️ archive/ - アーカイブ
使用頻度の低いファイル・履歴保存

#### 2024_powerarq_faq/ - PowerArQ FAQ更新履歴
#### article_backups/ - 記事バックアップ
#### temp_scripts/ - 一時的なスクリプト
#### special_articles/ - 特別な記事

## 🚀 よく使うコマンド

### 基本的な記事更新
```bash
cd /Users/g.ohorudingusu/Docbase/core
./update_docbase.sh
```

### LP欄生成
```bash
cd /Users/g.ohorudingusu/Docbase/lp_generator
./run_lp_generator.sh
```

### FAQ管理
```bash
cd /Users/g.ohorudingusu/Docbase/faq_tools
python faq_flag_manager.py
```

## ⚙️ 環境設定

### 初回セットアップ
```bash
# 仮想環境を有効化
source /Users/g.ohorudingusu/Docbase/core/docbase_env/bin/activate

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