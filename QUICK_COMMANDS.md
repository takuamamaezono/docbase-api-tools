# Hammerspoon & Docbase クイックコマンド集

## 🚀 即座に使えるコマンド

### Hammerspoonプラグイン作成
```bash
# 新しいプラグイン作成
cat > ~/.hammerspoon/new_plugin.lua << 'EOF'
-- New Plugin Template
local obj = {}

-- 設定
local hotkey = "cmd-shift-x"
local app_name = "Target App"

local function showChooser()
    hs.alert.show("New Plugin Activated!")
end

hs.hotkey.bind("cmd", "shift", "x", showChooser)
hs.alert.show("🎨 New Plugin loaded\\n⌨️ " .. hotkey)

return obj
EOF

# init.luaに追加
echo 'require("new_plugin")' >> ~/.hammerspoon/init.lua

# Hammerspoon再起動
open -a "Hammerspoon"
```

### Docbase記事作成
```bash
# Docbase環境に移動
cd /Users/g.ohorudingusu/Docbase

# 仮想環境有効化
source docbase_env/bin/activate

# 新規記事作成
python create_new_article.py "記事タイトル" article.md "tag1,tag2"

# 記事一覧確認
./docbase_helper.sh list
```

## 📝 テンプレート生成コマンド

### Hammerspoonプラグインテンプレート生成
```bash
create_hammerspoon_plugin() {
    local plugin_name=$1
    local app_name=$2
    local hotkey=$3
    
    cat > ~/.hammerspoon/${plugin_name}.lua << EOF
-- ${plugin_name} Plugin for Hammerspoon
local obj = {}
obj.name = "${plugin_name}"
obj.version = "1.0"

local hotkey = "${hotkey:-cmd-shift-x}"
local app_name = "${app_name:-Target Application}"

local menu_items = {
    {"Sample Action", {"Menu", "SubMenu", "Action"}, "🔧"},
}

local chooser = nil

local function getTargetApp()
    return hs.application.find(app_name)
end

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
        end
    end)
end

local function buildChoices()
    local choices = {}
    for _, item in ipairs(menu_items) do
        table.insert(choices, {
            text = (item[3] or "🔧") .. " " .. item[1],
            subText = "メニュー: " .. table.concat(item[2], " > "),
            path = item[2]
        })
    end
    return choices
end

local function chooserCallback(choice)
    if choice then executeMenuItem(choice.path) end
end

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

hs.hotkey.bind("cmd", "shift", "x", showChooser)
hs.alert.show("🎨 ${plugin_name} が読み込まれました\\n⌨️ ${hotkey}")

return obj
EOF

    echo "require(\"${plugin_name}\")" >> ~/.hammerspoon/init.lua
    echo "✅ ${plugin_name}プラグインを作成しました"
}

# 使用例
# create_hammerspoon_plugin "photoshop_helper" "Adobe Photoshop" "cmd-shift-p"
```

### Docbase記事テンプレート生成
```bash
create_docbase_article_template() {
    local title=$1
    local app_name=$2
    local hotkey=$3
    local filename="${title,,}"
    filename="${filename// /_}_guide.md"
    
    cat > "/Users/g.ohorudingusu/Docbase/${filename}" << EOF
# ${title} - Hammerspoon実装ガイド

## 概要
${app_name}用のSpotlight風検索プラグインです。よく使う機能を素早くアクセスできます。

## 主な機能
### 1. メニュー検索機能
- よく使う機能を瞬時に検索
- 絵文字アイコンで視覚的に分かりやすく表示

### 2. 高速アクセス
- キーボードショートカットのみで操作完了
- 日本語での検索に完全対応

## インストールと設定
### 前提条件
- macOS環境
- Hammerspoon がインストールされていること
- ${app_name} がインストールされていること

### セットアップ手順
1. ファイルの配置
2. Hammerspoon設定の更新
3. アクセシビリティ権限の設定

## 使用方法
### 起動ショートカット
\`\`\`
${hotkey}
\`\`\`

### 基本操作
1. ショートカットキーでプラグインを起動
2. 検索窓に機能名を入力
3. 上下矢印キーで項目を選択
4. Enterキーで実行

## 対応機能一覧
### カテゴリ1
- 機能1
- 機能2

### カテゴリ2
- 機能3
- 機能4

## カスタマイズ方法
### メニュー項目の追加
\`\`\`lua
{"新しい機能", {"メニューパス"}, "🆕"},
\`\`\`

### ホットキーの変更
\`\`\`lua
local hotkey = "cmd-shift-新しいキー"
\`\`\`

## トラブルシューティング
### プラグインが動作しない場合
1. Hammerspoonの状態確認
2. アクセシビリティ権限の確認
3. ${app_name}の状態確認

## 技術仕様
### 開発言語・環境
- 言語: Lua
- 実行環境: Hammerspoon
- 対象OS: macOS

## サポート情報
- 開発者: G.O（Claude Code支援）
- 更新日: $(date +%Y年%m月%d日)
- バージョン: 1.0
EOF

    echo "✅ ${filename} を作成しました"
    echo "📝 ファイルパス: /Users/g.ohorudingusu/Docbase/${filename}"
}

# 使用例
# create_docbase_article_template "Photoshop Helper" "Adobe Photoshop" "Cmd + Shift + P"
```

## 🔧 デバッグ・確認コマンド

### Hammerspoon状態確認
```bash
# Hammerspoonログ確認
tail -f ~/.hammerspoon/hammerspoon.log

# 設定ファイルの構文チェック
lua -c "dofile('/Users/g.ohorudingusu/.hammerspoon/init.lua')" 2>&1 || echo "文法エラーあり"

# アクセシビリティ権限確認
osascript -e 'tell application "System Events" to get processes where visible is true'
```

### Docbase環境確認
```bash
# API権限テスト
test_docbase_api() {
    cd /Users/g.ohorudingusu/Docbase
    source docbase_env/bin/activate
    python -c "
import os, requests
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('DOCBASE_ACCESS_TOKEN')
team = os.getenv('DOCBASE_TEAM')
url = f'https://api.docbase.io/teams/{team}/posts'
headers = {'X-DocBaseToken': token}
response = requests.get(url, headers=headers)
print(f'API Status: {response.status_code}')
if response.status_code == 200:
    posts = response.json()
    print(f'記事数: {len(posts[\"posts\"])}件')
else:
    print(f'エラー: {response.text}')
"
}

# 環境変数確認
check_docbase_env() {
    cd /Users/g.ohorudingusu/Docbase
    source docbase_env/bin/activate
    python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('Token:', os.getenv('DOCBASE_ACCESS_TOKEN')[:10] + '...' if os.getenv('DOCBASE_ACCESS_TOKEN') else 'Not found')
print('Team:', os.getenv('DOCBASE_TEAM'))
"
}
```

## ⚡ ワンライナーコマンド

### 完全な作業フロー（1コマンド）
```bash
# プラグイン名、アプリ名、ホットキーを指定して完全作成
create_complete_plugin() {
    local plugin_name=$1
    local app_name=$2  
    local hotkey=$3
    
    echo "🚀 ${plugin_name}プラグインを作成中..."
    
    # 1. Hammerspoonプラグイン作成
    create_hammerspoon_plugin "$plugin_name" "$app_name" "$hotkey"
    
    # 2. Docbase記事テンプレート作成
    create_docbase_article_template "$plugin_name Guide" "$app_name" "$hotkey"
    
    # 3. Hammerspoon再起動
    open -a "Hammerspoon"
    
    echo "✅ 完了！"
    echo "📝 次のステップ: 記事を編集してDocbaseにアップロード"
    echo "cd /Users/g.ohorudingusu/Docbase && source docbase_env/bin/activate"
    echo "python create_new_article.py '${plugin_name} Guide' ${plugin_name,,}_guide.md 'tag1,tag2'"
}

# 使用例
# create_complete_plugin "InDesign Helper" "Adobe InDesign" "Cmd + Shift + D"
```

### 記事アップロード（1コマンド）
```bash
# ファイル名から自動でタイトルを生成してアップロード
upload_guide() {
    local filename=$1
    local tags=${2:-"Hammerspoon,macOS,プラグイン"}
    
    cd /Users/g.ohorudingusu/Docbase
    source docbase_env/bin/activate
    
    # ファイル名からタイトルを生成
    local title=$(head -1 "$filename" | sed 's/^# //')
    
    python create_new_article.py "$title" "$filename" "$tags"
}

# 使用例
# upload_guide "photoshop_helper_guide.md" "Hammerspoon,Adobe,Photoshop"
```

## 📋 成功パターンのコピペ用

### Illustrator Plugin成功パターン
```bash
# Illustrator Search Plugin（成功例）
# ショートカット: Cmd+Alt+I （Cmd+Shift+Iから競合回避のため変更）
cat > ~/.hammerspoon/illustrator_search.lua << 'EOF'
# [成功したコードをここにペースト]
EOF

echo 'require("illustrator_search")' >> ~/.hammerspoon/init.lua
open -a "Hammerspoon"
```

### 記事作成成功パターン
```bash
cd /Users/g.ohorudingusu/Docbase
source docbase_env/bin/activate
python create_new_article.py "Adobe Illustrator Search Plugin - Hammerspoon実装ガイド" guide.md "Hammerspoon,Adobe Illustrator,macOS,プラグイン,効率化ツール"
```

---

これらのコマンドをコピペするだけで、次回は5分でプラグイン作成からDocbase記事化まで完了できます！