# Hammerspoonプラグイン作成＆Docbase記事化 完全ガイド

## 概要
Hammerspoonプラグインの実装からDocbase記事作成までの完全な作業フローをまとめたガイドです。

## 🚀 基本作業フロー

### 1. プラグイン実装
```bash
# Hammerspoonプラグインファイルを作成
~/.hammerspoon/plugin_name.lua

# init.luaに追加
echo 'require("plugin_name")' >> ~/.hammerspoon/init.lua

# Hammerspoon設定リロード
open -a "Hammerspoon"
# または
hs -c "hs.reload()"
```

### 2. Docbase記事作成
```bash
cd /Users/g.ohorudingusu/Docbase

# 新規記事作成（推奨方法）
source docbase_env/bin/activate
python create_new_article.py "記事タイトル" article_file.md "タグ1,タグ2,タグ3"

# または既存記事更新
./docbase_helper.sh update 記事ID content.md
```

## 📝 Hammerspoonプラグインテンプレート

### 基本構造
```lua
-- Plugin Name for Hammerspoon
-- アプリケーション操作プラグイン

local obj = {}
obj.__index = obj

-- プラグイン情報
obj.name = "PluginName"
obj.version = "1.0"
obj.author = "Claude & User"

-- 設定
local hotkey = "cmd-shift-x"  -- 起動ホットキー
local app_name = "Target Application"

-- メニュー項目リスト
local menu_items = {
    {"表示名", {"メニュー", "サブメニュー", "項目"}, "🔧"},
    {"別の機能", {"別メニュー", "項目"}, "⚡"},
}

-- 検索用のChooser変数
local chooser = nil

-- アプリケーション取得
local function getTargetApp()
    return hs.application.find(app_name)
end

-- メニュー項目実行
local function executeMenuItem(path)
    local app = getTargetApp()
    if not app then
        hs.alert.show(app_name .. "が起動していません")
        return
    end
    
    app:activate()
    hs.timer.doAfter(0.1, function()
        local success = app:selectMenuItem(path)
        if success then
            hs.alert.show("実行: " .. table.concat(path, " > "))
        else
            hs.alert.show("メニューが見つかりません")
        end
    end)
end

-- Choices配列作成
local function buildChoices()
    local choices = {}
    
    for _, item in ipairs(menu_items) do
        table.insert(choices, {
            text = (item[3] or "🔧") .. " " .. item[1],
            subText = "メニュー: " .. table.concat(item[2], " > "),
            path = item[2],
            type = "menu"
        })
    end
    
    return choices
end

-- Chooserコールバック
local function chooserCallback(choice)
    if choice then
        executeMenuItem(choice.path)
    end
end

-- 検索インターフェース表示
local function showChooser()
    local app = getTargetApp()
    if not app then
        hs.alert.show(app_name .. "が起動していません")
        return
    end
    
    if not chooser then
        chooser = hs.chooser.new(chooserCallback)
        chooser:choices(buildChoices())
        chooser:searchSubText(true)
        chooser:placeholderText(app_name .. "のメニューを検索...")
    end
    
    chooser:show()
end

-- ホットキー設定
hs.hotkey.bind("cmd", "shift", "x", showChooser)

-- 読み込み完了通知
hs.alert.show("🎨 " .. obj.name .. " が読み込まれました\\n⌨️ " .. hotkey .. " で起動")

return obj
```

## 🛠️ Docbase記事テンプレート

### 記事構成
```markdown
# [アプリ名] [機能名] - Hammerspoon実装ガイド

## 概要
プラグインの概要と目的

## 主な機能
### 1. 機能1
### 2. 機能2
### 3. 機能3

## インストールと設定
### 前提条件
### セットアップ手順

## 使用方法
### 起動ショートカット
### 基本操作
### 検索のコツ

## 対応機能一覧
### カテゴリ1
### カテゴリ2

## カスタマイズ方法
### 項目の追加
### ホットキーの変更

## トラブルシューティング
### よくある問題と解決方法

## 技術仕様
### 開発環境
### アーキテクチャ
### パフォーマンス

## 今後の拡張予定
### 機能拡張
### 対応アプリ拡張

## ライセンスと利用条件

## サポート情報
```

## 🔧 必要なファイルとスクリプト

### Docbase環境
```bash
# 環境変数設定 (.env)
DOCBASE_ACCESS_TOKEN=your_token_here
DOCBASE_TEAM=go

# 仮想環境
source /Users/g.ohorudingusu/Docbase/docbase_env/bin/activate

# 必須スクリプト
/Users/g.ohorudingusu/Docbase/create_new_article.py  # 新規記事作成
/Users/g.ohorudingusu/Docbase/docbase_helper.py      # 既存記事操作
/Users/g.ohorudingusu/Docbase/docbase_helper.sh      # 簡単操作
```

### Hammerspoon環境
```bash
# メインディレクトリ
~/.hammerspoon/

# 必須ファイル
~/.hammerspoon/init.lua              # メイン設定
~/.hammerspoon/plugin_name.lua      # プラグイン本体

# 確認コマンド
which hs                             # Hammerspoonコマンド確認
open -a "Hammerspoon"               # アプリ起動
```

## ⚡ 作業時のクイックコマンド

### プラグイン作成から記事化まで
```bash
# 1. プラグイン作成
vim ~/.hammerspoon/new_plugin.lua

# 2. init.luaに追加
echo 'require("new_plugin")' >> ~/.hammerspoon/init.lua

# 3. Hammerspoon再起動
open -a "Hammerspoon"

# 4. 記事ファイル作成
vim /Users/g.ohorudingusu/Docbase/new_plugin_guide.md

# 5. Docbase記事作成
cd /Users/g.ohorudingusu/Docbase
source docbase_env/bin/activate
python create_new_article.py "新プラグインガイド" new_plugin_guide.md "タグ1,タグ2"
```

### よく使うDocbase操作
```bash
# 記事一覧表示
./docbase_helper.sh list

# 記事取得
./docbase_helper.sh get 記事ID

# セクション追加
./docbase_helper.sh add-section 記事ID "セクション名" "内容"

# 記事更新
./docbase_helper.sh update 記事ID content.md
```

## 🎯 成功パターンの実例

### Illustrator Search Plugin
- **ショートカット**: `Cmd + Alt + I` （`Cmd + Shift + I`から変更）
- **記事ID**: 3890202
- **成功要因**: 
  - 既存の動作環境を活用
  - 過去の成功パターンを踏襲
  - 詳細なドキュメント作成
  - 競合問題の迅速な解決

## 🚨 注意点・トラブル対策

### Hammerspoon関連
- アクセシビリティ権限の確認
- init.luaの構文エラーチェック
- アプリケーション名の正確性
- **ショートカット競合の確認**（重要！）
  - `Cmd+Shift+I`は多くのアプリで使用されている
  - `Cmd+Alt`系列の方が競合しにくい
  - 動作しない場合は別のキーに変更を検討

### Docbase関連
- scope設定は必ず "private"
- 環境変数の正確性確認
- API権限の確認

### 一般的な問題
```bash
# Hammerspoon設定エラー
tail -f ~/.hammerspoon/hammerspoon.log

# Docbase API権限確認
source docbase_env/bin/activate
python -c "
import os, requests
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('DOCBASE_ACCESS_TOKEN')
team = os.getenv('DOCBASE_TEAM')
url = f'https://api.docbase.io/teams/{team}/posts'
headers = {'X-DocBaseToken': token}
print('API Test:', requests.get(url, headers=headers).status_code)
"
```

## 📚 参考資料

- [Hammerspoon公式ドキュメント](https://www.hammerspoon.org/docs/)
- [Docbase API ドキュメント](https://help.docbase.io/posts/45703)
- [macOS Accessibility Programming Guide](https://developer.apple.com/documentation/accessibility)

## 🔄 更新履歴

- 2025/8/7: Illustrator Search Plugin成功パターンを追加
- 2025/8/7: ショートカット競合問題と解決方法を追加
- 2025/8/7: 初版作成

---

このガイドに従うことで、次回以降は効率的にHammerspoonプラグインの作成とDocbase記事化が可能です。