# Docbase タグ管理ガイド

## 概要

Docbaseの既存タグから選択して記事を作成・更新する機能です。新規タグの作成を防ぎ、既存タグの統一された管理を実現します。

## 主な特徴

### ✅ 既存タグのみ使用
- 新規タグの作成を防止
- 既存タグとの整合性チェック
- タグの重複・乱立を防止

### 🎯 インタラクティブ選択
- 利用可能なタグをリスト表示
- 番号選択による直感的な操作
- 複数タグの一括選択

### 🛡️ 安全な更新
- 記事更新時のタグ・設定保持
- 既存記事の設定変更なし
- バックアップ自動作成

## 使用方法

### 1. 既存タグの確認

```bash
# タグ一覧を表示
./docbase_tag_helper.sh tags

# または
python3 docbase_helper.py list-tags
```

**出力例：**
```
🏷️ 既存タグを取得中...
✅ 290 件のタグを取得しました

🏷️ 利用可能なタグ:
------------------------------------------------------------
  1. ラフ
  2. コスメ
  3. マニュアル
  4. SmartTap
  5. FIXIT
  6. amazon
  7. 楽天市場
  8. レポート
  9. ノウハウ
  ...
------------------------------------------------------------
```

### 2. インタラクティブ記事作成

```bash
# タグ選択付きで記事作成
./docbase_tag_helper.sh create "記事タイトル" article.md

# または
python3 docbase_helper.py create-interactive "記事タイトル" article.md
```

**操作フロー：**
1. 既存タグ一覧が表示される
2. 番号をカンマ区切りで入力（例: 1,3,5）
3. 選択されたタグで記事が作成される

**入力例：**
```
📝 タグ選択:
• 番号をカンマ区切りで入力してください (例: 1,3,5)
• Enterキーのみで選択せずに続行

選択する番号: 3,6,8

✅ 選択されたタグ: マニュアル, amazon, レポート
```

### 3. 記事更新（既存タグ保持）

```bash
# 記事内容のみ更新、タグ・設定は保持
./docbase_tag_helper.sh update 3891568 updated_article.md

# または
python3 docbase_helper.py update 3891568 updated_article.md
```

### 4. 記事取得・バックアップ

```bash
# 記事を取得してバックアップ作成
./docbase_tag_helper.sh get 3891568

# または
python3 docbase_helper.py get 3891568
```

## 従来の方式との比較

### 従来方式（タグ指定）
```bash
# 指定したタグが存在しない場合はスキップ
python3 docbase_helper.py create "記事タイトル" article.md "新タグ,amazon,マニュアル"
```

### 新方式（既存タグ選択）
```bash
# 既存タグから選択、新規タグ作成なし
python3 docbase_helper.py create-interactive "記事タイトル" article.md
```

## 実際の運用例

### 1. 在庫管理システム記事の作成

```bash
# 既存タグを確認
./docbase_tag_helper.sh tags | grep -E "(在庫|システム|マニュアル)"

# インタラクティブ選択で記事作成
./docbase_tag_helper.sh create "EF在庫管理システムガイド" ef_guide.md

# 選択例: システム開発, マニュアル, Google Apps Script, 在庫管理
```

### 2. 既存記事のブラッシュアップ

```bash
# 記事を取得
./docbase_tag_helper.sh get 3891568

# 内容を更新（タグはそのまま）
./docbase_tag_helper.sh update 3891568 updated_content.md
```

### 3. 複数記事の一括タグ統一

```bash
# 既存タグを確認してパターンを把握
./docbase_tag_helper.sh tags | grep -i "amazon"

# 各記事を統一されたタグで更新
./docbase_tag_helper.sh create "Amazon FBAガイド" fba.md
./docbase_tag_helper.sh create "Amazon在庫管理" inventory.md
# 同じタグ（amazon, マニュアル, 自動化システム）を選択
```

## 技術仕様

### API エンドポイント
- **タグ一覧取得**: `GET /teams/{team}/tags`
- **記事作成**: `POST /teams/{team}/posts`
- **記事更新**: `PATCH /teams/{team}/posts/{id}`

### データ構造
```json
{
  "name": "タグ名",
  "preferred": false,
  "starred": false
}
```

### 既存タグチェック機能
```python
# 指定されたタグが既存か確認
existing_tag_names = [tag['name'] for tag in all_tags]
valid_tags = [tag for tag in specified_tags if tag in existing_tag_names]
```

## トラブルシューティング

### タグが見つからない場合
```
⚠️ 存在しないタグをスキップ: 新しいタグ名
✅ 既存タグを適用: amazon, マニュアル
```

### 認証エラー
```bash
# 環境変数を確認
echo $DOCBASE_ACCESS_TOKEN

# .envファイルを確認
cat .env
```

### ファイルが見つからない
```bash
# ファイルの存在確認
ls -la article.md

# 絶対パスで指定
./docbase_tag_helper.sh create "タイトル" /full/path/to/article.md
```

## ベストプラクティス

### 1. タグ選択の指針
- **用途別**: システム開発, マニュアル, レポート
- **技術別**: Google Apps Script, Python, JavaScript
- **部門別**: amazon, 楽天市場, 営業

### 2. 記事作成の手順
1. 既存タグを確認してカテゴリを把握
2. 適切なタグ組み合わせを選択
3. インタラクティブモードで記事作成
4. 必要に応じて内容更新

### 3. タグ管理のルール
- 新規タグは原則作成しない
- 類似タグがある場合は既存を使用
- 定期的にタグ一覧を見直し

## 今後の拡張予定

### 機能拡張
- [ ] タグのカテゴリ別フィルタリング
- [ ] よく使うタグの優先表示
- [ ] タグ使用頻度の分析
- [ ] 記事一覧でのタグ検索連携

### UI改善
- [ ] タグ選択のプレビュー機能
- [ ] 選択済みタグのハイライト表示
- [ ] タグ組み合わせの提案機能

---

**📅 作成日**: 2025年8月26日  
**🔄 更新履歴**: 初版作成  
**👤 作成者**: Claude Code System