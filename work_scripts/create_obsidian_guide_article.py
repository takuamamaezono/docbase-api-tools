#!/usr/bin/env python3
"""
Obsidian × Claude Code × Gemini CLI活用ガイド記事をDocbaseに投稿するスクリプト
"""

import requests
import json
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

class DocBaseCreator:
    def __init__(self, team_name: str, access_token: str):
        """
        DocBase APIクライアントを初期化
        
        Args:
            team_name: チーム名 (例: 'go')
            access_token: APIアクセストークン
        """
        self.team_name = team_name
        self.access_token = access_token
        self.base_url = "https://api.docbase.io"
        self.headers = {
            "X-DocBaseToken": access_token,
            "Content-Type": "application/json"
        }
    
    def create_post(self, title: str, body: str, tags: list = None, scope: str = "private") -> bool:
        """
        新しい記事を作成
        
        Args:
            title: 記事のタイトル
            body: 記事の本文
            tags: タグのリスト
            scope: 公開範囲 ('everyone', 'group', 'private')
            
        Returns:
            作成が成功したかどうか
        """
        url = f"{self.base_url}/teams/{self.team_name}/posts"
        
        # 作成データを準備
        post_data = {
            "title": title,
            "body": body,
            "scope": scope  # ルールに従い、私的設定にする
        }
        
        if tags:
            post_data["tags"] = tags
        
        try:
            response = requests.post(url, headers=self.headers, json=post_data)
            response.raise_for_status()
            result = response.json()
            print(f"記事の作成に成功しました！")
            print(f"記事ID: {result.get('id')}")
            print(f"URL: {result.get('url')}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"記事の作成に失敗しました: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"エラー詳細: {e.response.text}")
            return False

def load_article_content():
    """
    Obsidianガイド記事のコンテンツを読み込む
    """
    article_path = "/Users/g.ohorudingusu/obsidian-claude-gemini-docbase-guide.md"
    
    try:
        with open(article_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"記事コンテンツを読み込みました（{len(content)}文字）")
        return content
    except FileNotFoundError:
        print(f"記事ファイルが見つかりません: {article_path}")
        return None
    except Exception as e:
        print(f"記事ファイルの読み込みに失敗しました: {e}")
        return None

def main():
    """メイン関数"""
    
    # 環境変数から設定を読み込む
    TEAM_NAME = os.getenv("DOCBASE_TEAM", "go")  # チーム名
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")  # APIトークン
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        print("\n以下の方法で設定してください：")
        print("1. .envファイルをコピーして設定:")
        print("   cp .env.example .env")
        print("   # .envファイルを編集してAPIトークンを設定")
        print("\n2. または環境変数を直接設定:")
        print("   export DOCBASE_ACCESS_TOKEN='あなたのアクセストークン'")
        return
    
    # 記事コンテンツを読み込み
    content = load_article_content()
    if not content:
        return
    
    # DocBaseクライアントを作成
    client = DocBaseCreator(TEAM_NAME, ACCESS_TOKEN)
    
    # 記事情報
    title = "Obsidian × Claude Code × Gemini CLI 完全活用ガイド"
    tags = ["AI", "ツール", "Obsidian", "Claude Code", "Gemini CLI", "ワークフロー", "知識管理"]
    
    print(f"=== 記事作成情報 ===")
    print(f"タイトル: {title}")
    print(f"文字数: {len(content)}")
    print(f"タグ: {', '.join(tags)}")
    print(f"公開範囲: private（従業員のみ）")
    print("=" * 50)
    
    # 自動実行するよう変更
    print("\n記事を作成します...")
    # confirm = input("\n記事を作成しますか？ (y/N): ")
    # if confirm.lower() != 'y':
    #     print("記事作成をキャンセルしました")
    #     return
    
    # 記事を作成
    success = client.create_post(
        title=title,
        body=content,
        tags=tags,
        scope="private"  # ルールに従い私的設定
    )
    
    if success:
        print("\n✅ 記事の作成が完了しました！")
        print("チームメンバーがDocbaseで確認できます。")
    else:
        print("\n❌ 記事の作成に失敗しました。")

if __name__ == "__main__":
    main()