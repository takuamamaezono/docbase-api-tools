#!/bin/bash

# Docbase タグ管理ヘルパースクリプト
# 既存タグから選択してDocbase記事を作成・更新

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HELPER_SCRIPT="$SCRIPT_DIR/docbase_helper.py"

show_usage() {
    echo "📝 Docbase タグ管理ヘルパー"
    echo ""
    echo "使い方:"
    echo "  $0 tags                           # 既存タグ一覧を表示"
    echo "  $0 create <タイトル> <bodyファイル>  # インタラクティブにタグ選択して記事作成"
    echo "  $0 update <記事ID> <bodyファイル>   # 既存記事を更新（タグはそのまま）"
    echo "  $0 get <記事ID>                   # 記事を取得・バックアップ"
    echo ""
    echo "特徴:"
    echo "  ✅ 既存タグのみ使用（新規タグ作成不可）"
    echo "  🎯 インタラクティブなタグ選択"
    echo "  🛡️ 安全な記事更新（既存設定保持）"
    echo ""
    echo "例:"
    echo "  $0 tags                                    # 利用可能なタグを確認"
    echo "  $0 create \"新機能マニュアル\" article.md     # タグ選択して記事作成"
    echo "  $0 update 3891568 updated_article.md      # 記事内容のみ更新"
}

if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

command="$1"

case "$command" in
    "tags"|"list-tags")
        echo "🏷️ 既存タグ一覧を取得中..."
        python3 "$HELPER_SCRIPT" list-tags
        ;;
    "create")
        if [ $# -lt 3 ]; then
            echo "❌ エラー: タイトルとボディファイルが必要です"
            echo "使い方: $0 create <タイトル> <bodyファイル>"
            exit 1
        fi
        
        title="$2"
        body_file="$3"
        
        if [ ! -f "$body_file" ]; then
            echo "❌ エラー: ファイル '$body_file' が見つかりません"
            exit 1
        fi
        
        echo "📝 インタラクティブタグ選択で記事作成..."
        python3 "$HELPER_SCRIPT" create-interactive "$title" "$body_file"
        ;;
    "update")
        if [ $# -lt 3 ]; then
            echo "❌ エラー: 記事IDとボディファイルが必要です"
            echo "使い方: $0 update <記事ID> <bodyファイル>"
            exit 1
        fi
        
        article_id="$2"
        body_file="$3"
        
        if [ ! -f "$body_file" ]; then
            echo "❌ エラー: ファイル '$body_file' が見つかりません"
            exit 1
        fi
        
        echo "📝 記事更新（タグ・設定は保持）..."
        python3 "$HELPER_SCRIPT" update "$article_id" "$body_file"
        ;;
    "get")
        if [ $# -lt 2 ]; then
            echo "❌ エラー: 記事IDが必要です"
            echo "使い方: $0 get <記事ID>"
            exit 1
        fi
        
        article_id="$2"
        echo "📖 記事取得中..."
        python3 "$HELPER_SCRIPT" get "$article_id"
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        echo "❌ 無効なコマンド: $command"
        echo ""
        show_usage
        exit 1
        ;;
esac