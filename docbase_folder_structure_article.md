# 🛍️ PowerArQ Shopify開発環境 - フォルダ構成完全ガイド

## 📋 記事概要

**対象読者**: PowerArQ Shopify開発チーム、今後の担当者  
**目的**: 整理済みShopify開発環境の理解と効率的活用  
**最終更新**: 2025年8月23日

---

## 🗂️ フォルダ構成全体像

PowerArQ Shopifyの開発フォルダ（`/Users/g.ohorudingusu/Work/Shopify/`）は、機能別・用途別に以下の構成で整理されています。

```
/Users/g.ohorudingusu/Work/Shopify/
├── 📁 メインプロジェクト/
│   ├── top_header/                    # PowerArQ TOPバナー自動システム（本番稼働中）
│   ├── shopify-banner-system/         # バナーシステム配布版
│   ├── shopify-sale-banner-system/    # セールページ監視システム
│   └── shopify-comprehensive-sale-system/ # セール総合管理システム
├── 📁 サポート環境/
│   ├── shopify---powearq/            # 本家テーマファイルリポジトリ
│   ├── docs/                         # プロジェクト文書（機能別分類）
│   ├── archive/                      # バックアップ・旧ファイル
│   └── shopify_env/                  # Python実行環境
├── 🔧 汎用ツール（直下）/
│   ├── bulk_update_meta.py           # 商品メタ情報一括更新
│   ├── list_all_products.py          # 全商品一覧取得
│   ├── find_product_by_handle.py     # 商品検索
│   └── その他の管理ツール...
├── ⚙️ 設定・ドキュメント/
│   ├── SHOPIFY_WORK_GUIDE.md         # 総合作業ガイド（必読）
│   ├── SHOPIFY_RULES.md              # 詳細作業ルール
│   └── meta_templates.json           # メタフィールドテンプレート
└── 🌐 環境設定/
    ├── .env                          # 環境変数（機密情報）
    └── .gitignore                    # Git管理除外設定
```

---

## 🎯 メインプロジェクト詳細

### **1. top_header/ - PowerArQ TOPバナーシステム**
**⚠️ 本番稼働中システム - 慎重に操作**

**役割**: PowerArQ公式サイトTOPページのバナー自動更新システム
**稼働状況**: 毎週金曜12:00に自動実行中
**管理対象**: ICEBERG 12L含む5商品のバナー

**主要ファイル**:
- `auto_banner_system_enhanced.py` - 本番自動実行システム
- `check_current_banners.py` - 現在のバナー状況確認
- `add_iceberg_12l_banner.py` - ICEBERG 12L手動追加
- `setup_weekly_cron.sh` - 定期実行設定

**操作時の注意**:
```bash
# 作業前に必ず現状確認
cd top_header
python3 check_current_banners.py

# テスト環境での確認後に本番実行
python3 auto_banner_system_enhanced.py
```

### **2. shopify-banner-system/ - バナーシステム配布版**
**役割**: PowerArQバナーシステムの整理済みGitHubリポジトリ
**特徴**:
- 不要ファイル除去済みのクリーン版
- GitHub: https://github.com/takuamamaezono/shopify-banner-system
- Docbase記事: https://go.docbase.io/posts/3903386

**用途**: 他の開発者への引き継ぎ、ドキュメント用途

### **3. shopify-sale-banner-system/ - セールページ監視システム**
**役割**: セールページ（collections/sale）のカウントダウンタイマー監視
**監視対象**: 72商品のセールページ
**機能**:
- タイマー動作の自動チェック・修正
- セール設定の監視・報告

**設定ファイル**:
- `summer_sale_config.json` - 夏季セール設定
- `weekend_sale_config.json` - 週末セール設定

### **4. shopify-comprehensive-sale-system/ - セール総合管理**
**役割**: セール機能全般の包括的開発・管理環境
**特徴**:
- セール実行、診断、修正の統合システム
- 開発履歴とアーカイブを含む
- より広範囲なセール管理機能

**構成**:
```
shopify-comprehensive-sale-system/
├── scripts/                    # 実行スクリプト
├── configs/                    # 設定ファイル
├── logs/                       # 実行ログ
└── README.md                   # クイックスタートガイド
```

---

## 📁 サポート環境

### **docs/ - プロジェクト文書管理**
**機能別分類による整理**:
```
docs/
├── sale_execution/              # セール実行関連
│   ├── FINAL_EXECUTION_GUIDE.md
│   ├── QUICK_EXECUTION_GUIDE.md
│   └── CURRENT_SESSION_STATUS.md
├── system_design/               # システム設計・分析
│   └── CRITICAL_ISSUES_ANALYSIS.md
└── operational_guides/          # 継続運用ガイド
    ├── AUTOMATION_SYSTEM_DESIGN.md
    ├── MONTHLY_SALE_PROCESS.md
    └── SHOPIFY_SUMMER_SALE_MEMORY.md
```

### **archive/ - バックアップ・旧ファイル管理**
**分類別アーカイブ**:
```
archive/
├── backup_*_20250822_*.json     # API操作バックアップ（日付付き）
├── sale_banners_original/       # 旧セールバナーフォルダ
└── old_banner_work_20250823/    # 旧バナー作業ファイル
```

**命名規則**:
- 日付付きバックアップ: `filename_backup_YYYYMMDD_HHMMSS.ext`
- バージョン管理: `filename_v1.py`, `filename_v2.py`
- 説明付き: `説明_YYYYMMDD.ext`

---

## 🔧 汎用ツール（直下配置）

**配置理由**: プロジェクト横断で使用、独立性が高い

### **商品管理ツール群**
- `bulk_update_meta.py` - 商品メタ情報一括更新
- `list_all_products.py` - 全商品一覧取得
- `find_product_by_handle.py` - Handle名による商品検索
- `update_product_meta.py` - 個別商品メタ情報更新

### **セール・バナー関連ツール**
- `check_45l_banner.py` - PowerArQ 45Lバナー確認
- `fix_iceberg_countdown.py` - ICEBERGカウントダウン修正
- `get_sale_collection.py` - セールコレクション取得
- `auto_update_meta.py` - メタ情報自動更新

### **よく使用するワークフロー**
```bash
# 商品メタディスクリプション一括更新
source .env && source shopify_env/bin/activate
python bulk_update_meta.py

# 特定商品の詳細確認
python find_product_by_handle.py powerarq-2

# セール商品確認
python get_sale_collection.py
```

---

## ⚙️ 設定・ドキュメント管理

### **必読ドキュメント**
1. **`SHOPIFY_WORK_GUIDE.md`** - 総合作業ガイド
   - **最初に必ず読むファイル**
   - フォルダ構成、作業手順、トラブルシューティング

2. **`SHOPIFY_RULES.md`** - 詳細作業ルール
   - API使用ガイドライン、エラー対処法、セキュリティ注意事項

3. **`meta_templates.json`** - メタフィールドテンプレート
   - 商品カテゴリ別のメタディスクリプションテンプレート

### **重要設定ファイル**
- `.env` - 環境変数（機密情報 - GitHub管理対象外）
- `.gitignore` - Git管理除外設定

---

## 🐙 GitHub管理戦略

### **リポジトリ分類**
**システム特化リポジトリ**:
- shopify-banner-system
- shopify-sale-banner-system  
- shopify---powearq
- shopify-comprehensive-sale-system

**汎用ツール・ドキュメント管理**:
- shopify-powerarq-tools（汎用ツール集）
- shopify-workflow-docs（ドキュメント管理）

### **管理判定基準**
- **汎用性の高いツール** → `shopify-powerarq-tools` リポジトリ
- **特定システムに特化** → 該当システムリポジトリ  
- **ドキュメント・ガイド** → `shopify-workflow-docs` リポジトリ
- **実験・一時ファイル** → ローカル管理のみ

---

## 🚀 新規ファイル作成時のルール

### **配置判定フロー**
```
新規ファイル作成
    ↓
汎用ツール？
    ├─ Yes → 直下に配置 → GitHub: shopify-powerarq-tools
    └─ No → 特定プロジェクト？
        ├─ Yes → 該当プロジェクトフォルダ → GitHub: 該当リポジトリ
        └─ No → 実験・一時？
            ├─ Yes → archive/ → GitHub管理なし
            └─ No → ドキュメント？
                └─ Yes → docs/ → GitHub: shopify-workflow-docs
```

### **命名規則**
- **機能説明**: ファイル名から用途が明確に分かる
- **日付管理**: バックアップ・版数管理時は日付を含む
- **カテゴリ接頭辞**: 関連ファイルのグルーピングに活用

---

## ⚠️ 運用上の重要な注意事項

### **本番環境への影響**
- **`top_header/`**: 本番実行中システム（毎週金曜自動実行）
- **`shopify---powearq/`**: 本家テーマファイル（変更時要注意）

### **セキュリティ管理**
- **`.env` ファイル**: 機密情報管理、GitHub pushの厳禁
- **APIトークン**: 定期更新の実施
- **ログファイル**: 機密情報の混入チェック

### **API制限遵守**
- Shopify Admin APIのレート制限遵守
- 連続実行時は2秒間隔を推奨
- エラー時は適切な待機時間を設定

---

## 🔄 継続的なファイル管理

### **定期メンテナンス**
- **週次**: 不要ファイルの`archive/`移動
- **月次**: リポジトリ同期とドキュメント更新
- **四半期**: フォルダ構成の見直し

### **品質維持**
1. **新規作成時**: 必ず適切なフォルダに配置
2. **実験終了時**: 必要ファイルは適切な場所に移動、不要ファイルは削除
3. **プロジェクト完了時**: ドキュメント更新、GitHub同期

---

## 📚 関連リソース

### **Docbase記事**
- PowerArQバナーシステム: https://go.docbase.io/posts/3903386
- セールバナー監視システム: https://go.docbase.io/posts/3903387

### **GitHub リポジトリ一覧**
- システム特化: shopify-banner-system, shopify-sale-banner-system, shopify---powearq, shopify-comprehensive-sale-system
- 汎用・ドキュメント: shopify-powerarq-tools, shopify-workflow-docs

---

## 💡 今後の開発効率化

この整理された環境により期待される効果：

1. **作業開始時間の短縮**: 必要ファイルの場所が明確
2. **引き継ぎの円滑化**: 文書化された構成と手順
3. **品質向上**: 体系化されたツール群の活用
4. **リスク軽減**: バックアップとバージョン管理の徹底

**💪 このフォルダ構成を維持することで、PowerArQ Shopify開発の持続的な効率化を実現します！**

---

**📅 最終更新**: 2025年8月23日  
**👤 文書作成**: G.O Systems  
**🔄 次回レビュー予定**: 2025年9月23日