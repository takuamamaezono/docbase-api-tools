# Docbase クイックスタートガイド

## 🚀 今すぐ使える！簡単コマンド集

Docbaseの記事を更新する時は、以下のコマンドを使うだけでOK！

### よく使うコマンド

```bash
# 記事を取得してバックアップ
./docbase_helper.sh get 664151

# 記事にセクションを追加
./docbase_helper.sh add-section 664151 "新機能" "内容をここに"

# 記事一覧を見る
./docbase_helper.sh list

# PowerArQで検索
./docbase_helper.sh list PowerArQ
```

### 実際の使用例

#### 例1: バッテリー仕様を追加する場合
```bash
./docbase_helper.sh add-section 664151 "充電仕様" "45L側：10.8V(MAX12.6V)/2A(MAX3A)"
```

#### 例2: 記事全体を更新する場合
```bash
# 1. まず現在の記事を取得
./docbase_helper.sh get 664151

# 2. バックアップファイルを編集
# （article_664151_backup_日時.jsonが作成される）

# 3. 編集した内容で更新
./docbase_helper.sh update 664151 edited_content.md
```

### 💡 ポイント

1. **環境構築不要** - スクリプトが自動で環境をセットアップ
2. **改行コード対応** - Windows形式（\r\n）も自動処理
3. **バックアップ自動作成** - 更新前に必ずバックアップを作成
4. **エラー表示** - 問題があれば日本語でわかりやすく表示

### ⚠️ 初回のみ必要な設定

`.env`ファイルにAPIトークンが設定されているか確認：
```bash
cat .env
# DOCBASE_ACCESS_TOKEN=your_token_here が表示されればOK
```

### 📚 詳しい使い方

詳細は `./docbase_helper.sh` （引数なしで実行）でヘルプを表示できます。