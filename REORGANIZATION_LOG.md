# Docbaseフォルダ整理ログ

## 📅 実施日時
2025年1月31日

## 🎯 整理の目的
- 散乱していた60個以上のファイルを機能別に整理
- 使いやすいフォルダ構造に再編成
- LP欄自動生成システムの追加

## 📁 新しいフォルダ構造

```
Docbase/
├── README.md                      # 新規作成 - システム全体のガイド
├── REORGANIZATION_LOG.md          # 新規作成 - この整理ログ
├── core/                          # コア機能
│   ├── docbase_env/              # 移動元: ./docbase_env/
│   ├── docbase_updater.py        # 移動元: ./docbase_updater.py
│   ├── update_docbase_article.py # 移動元: ./update_docbase_article.py
│   ├── update_docbase.sh         # 移動元: ./update_docbase.sh
│   └── .env.example              # 新規作成
├── docs/                          # ドキュメント
│   ├── DOCBASE_RULES.md          # 移動元: ./DOCBASE_RULES.md
│   └── DOCBASE_API_GUIDE.md      # 移動元: ./DOCBASE_API_GUIDE.md
├── lp_generator/                  # LP生成システム（既存維持）
├── faq_tools/                     # FAQ管理ツール
│   ├── faq_flag_manager.py       # 移動元: ./faq_flag_manager.py
│   ├── FAQ_FLAG_GUIDE.md         # 移動元: ./FAQ_FLAG_GUIDE.md
│   ├── add_flags/                # フラグ追加系
│   ├── analyze/                  # 分析系（20個のファイル）
│   └── update/                   # 更新・修正系（18個のファイル）
├── manual_creators/               # マニュアル作成ツール
│   ├── asana/                    # Asana関連（6個のファイル）
│   ├── beginner/                 # 初心者向け（1個のファイル）
│   ├── chatbot/                  # チャットボット用（3個のファイル）
│   └── その他のツール（4個のファイル）
├── old_article_warning/           # 古い記事警告システム
│   └── 移動元: ./docbase_old_article_warning/
└── archive/                       # アーカイブ
    ├── 2024_powerarq_faq/        # PowerArQ FAQ更新履歴
    ├── article_backups/          # 記事バックアップ（10個のファイル）
    ├── temp_scripts/             # 一時的なスクリプト（5個のファイル）
    └── special_articles/         # 特別な記事（1個のファイル）
```

## 🔄 主要な移動・変更

### コア機能 (core/)
- `docbase_updater.py` - メイン更新スクリプト
- `update_docbase_article.py` - 個別記事更新
- `update_docbase.sh` - 実行シェル
- `docbase_env/` - Python仮想環境（そのまま）

### FAQ管理ツール (faq_tools/)
**add_flags/**: 2個のファイル
- `add_all_flags.py`
- `add_flags_test.py`

**analyze/**: 16個のファイル
- 分析・確認・比較系のスクリプト

**update/**: 18個のファイル
- FAQ構造変更・修正・再編成スクリプト

### マニュアル作成 (manual_creators/)
**asana/**: 6個のファイル
**beginner/**: 1個のファイル
**chatbot/**: 3個のファイル
**その他**: 4個のファイル

### アーカイブ (archive/)
**article_backups/**: 10個のデータファイル
- JSON、MD形式のバックアップファイル

**temp_scripts/**: 5個の一時スクリプト
- 作業用・一時的な処理スクリプト

**special_articles/**: 1個
- `営業先着事業部紹介記事.md`

## ✅ 整理完了項目

1. ✅ ファイル分析・分類完了
2. ✅ フォルダ構造作成完了
3. ✅ 全ファイル移動完了
4. ✅ ドキュメント作成完了
5. ✅ 環境設定ファイル作成完了

## 🚀 今後の使い方

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

## 📝 注意事項

- 古いパスを使用しているスクリプトがある場合は、新しいパスに更新が必要
- `.env`ファイルは`core/`フォルダに配置
- アーカイブファイルも必要に応じて参照可能

## 🎯 整理効果

- **整理前**: 60個以上のファイルが散乱
- **整理後**: 機能別に7つのフォルダに分類
- **メリット**: 探しやすい、保守しやすい、使いやすい

---

整理担当: Claude Code
完了日時: 2025年1月31日