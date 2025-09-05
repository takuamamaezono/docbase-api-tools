# ⚡ Docbase古い記事への注意書き追加 - クイック実行ガイド

## 🎯 概要

このガイドは、Docbaseの1年以上古い記事に注意書きを追加する作業を**スムーズに実行**するための手順書です。

## 📋 前提条件

- Docbase APIアクセス権限
- Python環境（仮想環境推奨）
- 必要なパッケージ：`requests`, `python-dotenv`

## 🚀 5分で完了する実行手順

### Step 1: 環境準備
```bash
# Docbaseディレクトリに移動
cd /Users/g.ohorudingusu/Docbase

# 仮想環境をアクティベート
source docbase_env/bin/activate

# 古い記事警告システムディレクトリに移動
cd docbase_old_article_warning
```

### Step 2: 古い記事の検索
```bash
# 古い記事を検索・特定
python scripts/extended_search.py
```

**期待される結果:**
- `data/extended_old_articles.json` ファイルが生成
- 発見された古い記事の件数が表示

### Step 3: 注意書きの追加
```bash
# バッチ処理で注意書きを追加
python scripts/batch_warning_processor.py
```

**処理内容:**
- 10件ずつバッチで処理
- 既に追加済みの記事は自動スキップ
- 処理進捗をリアルタイム表示

### Step 4: 結果確認
処理完了後、以下が表示されます：
```
🎉 全バッチ処理完了！
📊 最終統計:
   対象記事数: XX 件
   注意書き追加: XX 件
   既に追加済み: XX 件
   完了率: 100.0%
```

## 📁 ファイル構成

```
docbase_old_article_warning/
├── scripts/
│   ├── extended_search.py           # 古い記事検索
│   ├── batch_warning_processor.py   # バッチ処理での注意書き追加
│   └── apply_warning_to_found_articles.py  # 個別処理用
├── docs/
│   ├── OLD_ARTICLE_WARNING_MANUAL.md        # 詳細マニュアル
│   ├── OLD_ARTICLE_WARNING_PROJECT_LOG.md   # 作業ログ
│   └── QUICK_EXECUTION_GUIDE.md             # このファイル
├── data/
│   └── extended_old_articles.json   # 発見された古い記事リスト
└── README.md                        # システム概要
```

## 🛠️ 各スクリプトの役割

### 1. extended_search.py
- **用途**: 1年以上古い記事の包括的検索
- **出力**: `data/extended_old_articles.json`
- **実行時間**: 約2-3分

### 2. batch_warning_processor.py
- **用途**: 発見された古い記事への注意書き一括追加
- **処理方式**: 10件ずつバッチ処理
- **実行時間**: 記事数によって変動（1件あたり約3秒）

### 3. apply_warning_to_found_articles.py
- **用途**: 個別記事への注意書き追加（テスト用）
- **オプション**: `--test`, `--execute`

## 📝 追加される注意書き

すべての対象記事の先頭に以下が追加されます：

```markdown
⚠️ **この記事は1年以上前に書かれたものです。情報が古い可能性があります。**

---
```

## 🔍 トラブルシューティング

### 問題1: 「extended_old_articles.json が見つかりません」
**原因**: Step 2の検索が完了していない
**解決**: `python scripts/extended_search.py` を再実行

### 問題2: APIエラー (401 Unauthorized)
**原因**: API認証情報の問題
**解決**: `.env` ファイルの `DOCBASE_ACCESS_TOKEN` を確認

### 問題3: 「記事なし」と表示される
**原因**: 該当期間に古い記事が存在しない
**対応**: 正常な状態です（すべて最新の記事）

### 問題4: 処理が途中で停止
**原因**: API制限またはネットワーク問題
**解決**: しばらく待ってから再実行（重複処理は自動で回避）

## ⏰ 定期実行の推奨

### 月次チェック
```bash
# 毎月末に実行推奨
cd /Users/g.ohorudingusu/Docbase/docbase_old_article_warning
python scripts/extended_search.py
```

### 新しい古い記事が見つかった場合
```bash
python scripts/batch_warning_processor.py
```

## 📊 実行ログの確認

### 実行履歴
- 前回実行結果は `docs/OLD_ARTICLE_WARNING_PROJECT_LOG.md` に記録
- 各実行時の統計情報を確認可能

### 対象記事の確認
- `data/extended_old_articles.json` で詳細確認
- 記事ID、タイトル、更新日時、URL等を含む

## 🎯 成功の指標

✅ **正常完了の条件:**
- エラー 0件
- 完了率 100.0%
- 「全バッチ処理完了」メッセージ表示

✅ **品質確認:**
- 重複追加なし（自動チェック機能）
- 処理漏れなし（全件処理）
- 正確な条件適用（1年以上の記事のみ）

## 🚨 注意事項

1. **API制限**: 大量実行時は自動待機が入ります
2. **重複実行**: 既に追加済みの記事は自動スキップ
3. **バックアップ**: 重要な記事は事前にバックアップ推奨
4. **確認**: 処理後は実際の記事で結果を確認

## 📞 サポート

**システムトラブル時:**
- エラーメッセージをコピーして管理者に連絡
- `docs/OLD_ARTICLE_WARNING_MANUAL.md` で詳細確認

**カスタマイズ要望:**
- 注意書きテキストの変更
- 判定期間の調整（1年→6ヶ月等）
- 処理対象の絞り込み

---

**⚡ 5分で完了！古い記事への注意書き追加システム**  
**最終更新**: 2025年1月30日