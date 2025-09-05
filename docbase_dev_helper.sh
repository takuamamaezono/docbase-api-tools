#!/bin/bash

# Docbase操作を簡単にするヘルパースクリプト
# 仮想環境の自動有効化と基本的な操作をワンコマンドで実行

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境が存在しない場合はセットアップ
if [ ! -d "docbase_env" ]; then
    echo "🔧 初回セットアップを実行中..."
    bash setup_docbase_env.sh
fi

# 仮想環境を有効化
source docbase_env/bin/activate

# コマンドに応じて処理を実行
case "$1" in
    "get")
        if [ -z "$2" ]; then
            echo "❌ 記事IDを指定してください"
            echo "使い方: ./docbase_helper.sh get <記事ID>"
            exit 1
        fi
        python3 01_docbase_core/docbase_helper.py get "$2"
        ;;
    
    "update")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "❌ 記事IDと更新内容ファイルを指定してください"
            echo "使い方: ./docbase_helper.sh update <記事ID> <更新内容ファイル>"
            exit 1
        fi
        python3 01_docbase_core/docbase_helper.py update "$2" "$3"
        ;;
    
    "add-section")
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "❌ 記事ID、セクション名、内容を指定してください"
            echo "使い方: ./docbase_helper.sh add-section <記事ID> <セクション名> <内容>"
            exit 1
        fi
        python3 01_docbase_core/docbase_helper.py add-section "$2" "$3" "$4"
        ;;
    
    "replace")
        if [ -z "$2" ] || [ -z "$3" ] || [ -z "$4" ]; then
            echo "❌ 記事ID、置換前ファイル、置換後ファイルを指定してください"
            echo "使い方: ./docbase_helper.sh replace <記事ID> <old.txt> <new.txt>"
            exit 1
        fi
        python3 01_docbase_core/docbase_helper.py replace "$2" "$3" "$4"
        ;;
    
    "list")
        python3 01_docbase_core/docbase_helper.py list "$2"
        ;;
    
    "create")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "❌ タイトルと内容ファイルを指定してください"
            echo "使い方: ./docbase_helper.sh create <タイトル> <内容ファイル> [タグ1,タグ2]"
            exit 1
        fi
        python3 01_docbase_core/docbase_helper.py create "$2" "$3" "$4"
        ;;
    
    "quick-add")
        # よく使う更新パターン用のショートカット
        if [ -z "$2" ]; then
            echo "❌ 記事IDを指定してください"
            exit 1
        fi
        echo "📝 クイック追加モード"
        echo "追加する内容を入力してください（Ctrl+Dで終了）:"
        content=$(cat)
        
        # 一時ファイルに保存
        temp_file="/tmp/docbase_quick_add_$$.txt"
        echo "$content" > "$temp_file"
        
        # セクション名を聞く
        read -p "セクション名を入力: " section_name
        
        python3 01_docbase_core/docbase_helper.py add-section "$2" "$section_name" "$(cat $temp_file)"
        rm "$temp_file"
        ;;
    
    *)
        echo "📚 Docbase ヘルパー"
        echo ""
        echo "使い方:"
        echo "  ./docbase_helper.sh get <記事ID>                    # 記事を取得"
        echo "  ./docbase_helper.sh update <記事ID> <ファイル>      # 記事を更新"
        echo "  ./docbase_helper.sh add-section <記事ID> <名前> <内容>  # セクション追加"
        echo "  ./docbase_helper.sh replace <記事ID> <old> <new>    # セクション置換"
        echo "  ./docbase_helper.sh list [検索キーワード]           # 記事一覧"
        echo "  ./docbase_helper.sh create <タイトル> <ファイル> [タグ]  # 新規記事作成"
        echo "  ./docbase_helper.sh quick-add <記事ID>              # クイック追加"
        echo ""
        echo "例:"
        echo "  ./docbase_helper.sh get 664151"
        echo "  ./docbase_helper.sh add-section 664151 \"充電仕様\" \"10.8V/2A\""
        echo "  ./docbase_helper.sh create \"新記事タイトル\" \"記事内容.md\" \"Shopify,開発\""
        ;;
esac