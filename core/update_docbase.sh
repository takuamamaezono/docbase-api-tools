#!/bin/bash
# DocBase記事更新用のラッパースクリプト

echo "DocBase記事更新ツール"
echo "====================="

# 仮想環境を有効化
if [ -d "docbase_env" ]; then
    source docbase_env/bin/activate
else
    echo "仮想環境を作成中..."
    python3 -m venv docbase_env
    source docbase_env/bin/activate
    echo "必要なライブラリをインストール中..."
    pip install requests
fi

# アクセストークンの確認
if [ -z "$DOCBASE_ACCESS_TOKEN" ]; then
    echo "⚠️  アクセストークンが設定されていません"
    echo ""
    echo "以下のいずれかの方法でトークンを設定してください："
    echo ""
    echo "方法1: 環境変数で設定（一時的）"
    echo "  export DOCBASE_ACCESS_TOKEN='your-token-here'"
    echo ""
    echo "方法2: .envファイルを作成（永続的）"
    echo "  echo 'DOCBASE_ACCESS_TOKEN=your-token-here' > .env"
    echo ""
    echo "方法3: macOSキーチェーンに保存（最も安全）"
    echo "  security add-generic-password -s 'DocBase' -a 'API_TOKEN' -w"
    echo ""
    exit 1
fi

# .envファイルがあれば読み込む
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

# Pythonスクリプトを実行
python3 docbase_updater.py