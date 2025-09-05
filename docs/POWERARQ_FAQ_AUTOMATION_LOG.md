# PowerArQ FAQ自動反映システム 開発ログ

**作成日**: 2025年9月3日  
**最終更新**: 2025年9月3日

---

## 🎯 プロジェクト概要

### **目的**
AsanaのコメントからPowerArQ公式サイト（https://powerarq.com/pages/faq）への効率的なFAQ反映システムの構築

### **現在のステータス**
**Phase 1: 拡張機能開発** ✅ **完了**  
**Phase 2: Docbase整理・品質確認** 🔄 **進行中**  
**Phase 3: 自動反映システム** ⏸️ **検討中**

---

## 🔧 現在の実装状況

### **完了済み機能**

#### **1. Chrome拡張機能 v2.6** ✅
- **機能**: AsanaコメントからDocbaseFAQ記事への自動追記
- **場所**: `/Users/g.ohorudingusu/Development/Extensions/asana-docbase-extension/`
- **主要改善点**:
  - 「クリックして展開」内部への正確な挿入
  - 既存Docbase FAQ形式に完全統一（`#### Q:` + `**A:**`）
  - `- [ ] Web反映対象` チェックボックス自動追加
  - 不要な日付・区切り線削除

#### **2. Web反映FAQ抽出システム** ✅
- **機能**: `- [ ] Web反映対象` フラグに基づくFAQ自動抽出
- **場所**: `/Users/g.ohorudingusu/Development/Active/Docbase/manual_creators/web_sync_filter.py`
- **出力形式**: JSON、Markdown、HTML
- **統計機能**: 対象FAQ数、除外FAQ数の自動集計

### **現在のワークフロー**
```
Asana → Chrome拡張機能 → Docbase記事更新 → Web反映システム → FAQ抽出完了
                                                              ↓
                                                        手動実行待ち
                                                              ↓
                                               https://powerarq.com/pages/faq
```

---

## 🚧 今後の実装予定

### **Phase 3: 自動反映システム（検討中）**

#### **実装要件**
1. **「反映して」コマンドでの自動実行**
2. **PowerArQサイトへの安全な更新**
3. **バックアップ・ロールバック機能**

#### **技術的課題**
| 項目 | 現状 | 必要な調査 |
|------|------|-----------|
| **サイト管理システム** | 不明 | WordPress、Shopify、静的サイト等の特定 |
| **API アクセス** | 不明 | REST API、GraphQL等の利用可能性 |
| **認証方法** | 不明 | ログイン情報、APIキー等の確認 |
| **更新権限** | 不明 | 管理者権限の有無と範囲 |
| **現在の更新方法** | 不明 | 既存の更新フローの調査 |

#### **安全性要件**
- 自動バックアップ機能
- 更新失敗時のロールバック
- 段階的な更新テスト
- 管理者承認機能（オプション）

---

## 📁 Docbaseファイル構造

### **プロジェクト構成**
```
/Users/g.ohorudingusu/Development/Active/Docbase/
├── README.md                              # プロジェクト概要
├── docbase_helper.py                      # メイン操作ヘルパー
├── create_docbase_article.py             # 新規記事作成
├── .env                                   # 環境変数（機密情報）
├── .env.example                          # 環境変数テンプレート
│
├── core/                                  # 🔧 コア機能
│   ├── docbase_updater.py                # メイン記事更新スクリプト
│   ├── update_docbase_article.py         # 個別記事更新
│   └── update_docbase.sh                 # 実行用シェルスクリプト
│
├── docs/                                  # 📚 ドキュメント
│   ├── DOCBASE_RULES.md                  # 運用ルールと設定
│   └── DOCBASE_API_GUIDE.md              # API使用方法
│
├── faq_tools/                             # 🔍 FAQ管理システム
│   ├── faq_flag_manager.py               # フラグ管理メインツール
│   ├── FAQ_FLAG_GUIDE.md                 # フラグ機能ガイド
│   ├── add_flags/                        # Web反映フラグ追加機能
│   ├── analyze/                          # FAQ分析・比較・確認ツール
│   └── update/                           # FAQ構造変更・修正・再編成
│
├── manual_creators/                       # 📖 マニュアル作成ツール
│   ├── web_sync_filter.py                # ⭐ Web反映FAQ抽出システム
│   ├── asana/                            # Asana拡張機能マニュアル
│   ├── beginner/                         # 初心者向けマニュアル
│   └── chatbot/                          # チャットボット用コンテンツ
│
├── lp_generator/                          # 📝 LP欄生成システム
│   ├── run_lp_generator.sh               # LP生成実行スクリプト
│   ├── advanced_lp_generator.py          # 高機能LP生成
│   ├── competitor_analyzer.py            # 競合分析機能
│   └── templates/                        # テンプレートファイル
│
├── old_article_warning/                   # ⚠️ 古い記事警告システム
│   ├── add_warning_to_old_articles.py    # 警告追加スクリプト
│   └── QUICK_EXECUTION_GUIDE.md          # 実行ガイド
│
├── work_scripts/                          # ⚙️ 作業用スクリプト
│   ├── create_new_article.py             # 新規記事作成
│   ├── update_*.py                       # 各種更新スクリプト
│   └── get_article_*.py                  # 記事取得スクリプト
│
├── archive/                               # 🗄️ アーカイブ
│   ├── article_backups/                  # 記事バックアップ
│   ├── temp_scripts/                     # 一時的なスクリプト
│   └── special_articles/                 # 特別な記事
│
├── docbase_env/                           # Python仮想環境
├── whisper_env/                          # Whisper（音声認識）環境
└── backups/                              # バックアップファイル
```

### **主要機能別ファイル**

#### **📱 日常業務用**
- `faq_tools/faq_flag_manager.py` - FAQ管理
- `create_docbase_article.py` - 記事作成
- `manual_creators/web_sync_filter.py` - Web反映抽出

#### **🔧 システム管理**
- `core/update_docbase.sh` - 基本記事更新
- `docbase_helper.py` - 汎用ヘルパー
- `setup_docbase_env.sh` - 環境セットアップ

#### **🚀 自動化・生成**
- `lp_generator/run_lp_generator.sh` - LP欄生成
- `old_article_warning/` - 古い記事警告
- `work_scripts/create_new_article.py` - 新規記事作成

---

## 📊 開発成果

### **効果測定**
- **作業時間短縮**: 従来10分 → 現在30秒（拡張機能）
- **品質向上**: フォーマット統一、ミス削減
- **運用効率**: Web反映フラグ自動付与、抽出システム

### **対応記事**
1. **【PowerArQ】製品別FAQ - ポータブル冷蔵庫・サーキュレーター...** (ID: 2705590)
2. **【PowerArQ】製品別FAQ - ポータブル電源・ソーラーパネル** (ID: 707448)

---

## 🔄 次回アクション

### **Phase 3 実装前の調査項目**
1. **PowerArQサイト構造調査**
   - CMS種類の特定
   - API仕様の確認
   - 認証方式の調査

2. **安全性検証**
   - バックアップ手順の確立
   - テスト環境での動作確認
   - ロールバック機能の実装

3. **運用フロー設計**
   - 「反映して」コマンドの実装仕様
   - エラーハンドリング
   - ログ機能

### **技術的準備**
- PowerArQサイトのHTML構造分析
- 更新APIの調査・テスト
- 認証システムの整備

---

## 📝 備考

- **セキュリティ**: すべての機密情報は`.env`で管理
- **バックアップ**: 記事更新前に自動バックアップ作成
- **バージョン管理**: Git で履歴管理
- **権限**: すべての記事は「従業員のみ」で作成

---

**🎯 完成時のビジョン**: 
Asanaでの質問・回答 → ワンクリックでPowerArQ公式FAQに反映される完全自動化システム