#!/bin/bash

# Docbase環境セットアップスクリプト
# 毎回の環境構築を不要にするための初期設定

echo "🔧 Docbase環境をセットアップしています..."

# 仮想環境の確認と作成
if [ ! -d "docbase_env" ]; then
    echo "📦 仮想環境を作成中..."
    python3 -m venv docbase_env
fi

# 仮想環境を有効化
source docbase_env/bin/activate

# 必要なパッケージをインストール
echo "📚 必要なパッケージをインストール中..."
pip install --quiet --upgrade pip
pip install --quiet requests python-dotenv

# .envファイルが存在しない場合、テンプレートから作成
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "⚠️  .envファイルを作成しました。APIトークンを設定してください。"
    else
        # .env.exampleも作成
        cat > .env.example << 'EOF'
# Docbase API設定
DOCBASE_ACCESS_TOKEN=your_token_here
DOCBASE_TEAM=go
DOCBASE_POST_ID=記事ID
EOF
        echo "⚠️  .env.exampleを作成しました。.envファイルにコピーしてAPIトークンを設定してください。"
    fi
fi

echo "✅ 環境セットアップが完了しました！"
echo ""
echo "📝 使い方："
echo "  1. 記事を取得: ./docbase_helper.sh get <記事ID>"
echo "  2. 記事を更新: ./docbase_helper.sh update <記事ID> <更新内容ファイル>"
echo "  3. セクション追加: ./docbase_helper.sh add-section <記事ID> <セクション名> <内容>"