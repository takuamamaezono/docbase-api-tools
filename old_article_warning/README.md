# 📝 Docbase古い記事への注意書き追加システム

## 🎯 概要

1年以上更新されていないDocbase記事に自動で注意書きを追加するシステムです。

## ✨ 機能

- 🔍 **自動検索**: 1年以上古い記事を自動特定
- ⚠️ **注意書き追加**: 統一されたフォーマットで注意喚起
- 🚫 **重複回避**: 既に追加済みの記事は自動スキップ
- 📊 **バッチ処理**: 大量記事の効率的な一括処理
- 📈 **進捗表示**: リアルタイムの処理状況表示

## 🚀 クイックスタート

```bash
# 1. 環境準備
cd /Users/g.ohorudingusu/Docbase/docbase_old_article_warning
source ../docbase_env/bin/activate

# 2. 古い記事を検索
python scripts/extended_search.py

# 3. 注意書きを追加
python scripts/batch_warning_processor.py
```

## 📁 ディレクトリ構成

```
docbase_old_article_warning/
├── scripts/           # 実行スクリプト
├── docs/             # ドキュメント
├── data/             # データファイル
└── README.md         # このファイル
```

## 📊 実績

- **処理対象**: 65件の古い記事
- **成功率**: 100%
- **エラー**: 0件
- **最古記事**: 6年6ヶ月前

## 📖 ドキュメント

- **[クイック実行ガイド](QUICK_EXECUTION_GUIDE.md)**: 5分で完了する実行手順
- **[詳細マニュアル](docs/OLD_ARTICLE_WARNING_MANUAL.md)**: システムの詳細説明
- **[プロジェクトログ](docs/OLD_ARTICLE_WARNING_PROJECT_LOG.md)**: 開発・実行履歴

## 🔧 メンテナンス

**定期実行**: 月次での新しい古い記事チェックを推奨

---

**最終更新**: 2025年1月30日