#!/usr/bin/env python3
"""
DocBase記事更新スクリプト
使い方: python docbase_updater.py
"""

import requests
import json
import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

class DocBaseUpdater:
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
    
    def get_post(self, post_id: int) -> Optional[Dict[Any, Any]]:
        """
        記事の内容を取得
        
        Args:
            post_id: 記事のID
            
        Returns:
            記事の情報（辞書形式）、失敗時はNone
        """
        url = f"{self.base_url}/teams/{self.team_name}/posts/{post_id}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"記事の取得に失敗しました: {e}")
            return None
    
    def update_post(self, post_id: int, title: str = None, body: str = None, 
                   tags: list = None, scope: str = None) -> bool:
        """
        記事を更新
        
        Args:
            post_id: 記事のID
            title: 新しいタイトル（省略時は変更しない）
            body: 新しい本文（省略時は変更しない）
            tags: 新しいタグリスト（省略時は変更しない）
            scope: 公開範囲 ('everyone', 'group', 'private')
            
        Returns:
            更新が成功したかどうか
        """
        url = f"{self.base_url}/teams/{self.team_name}/posts/{post_id}"
        
        # 更新データを作成（指定されたフィールドのみ）
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if body is not None:
            update_data["body"] = body
        if tags is not None:
            update_data["tags"] = tags
        if scope is not None:
            update_data["scope"] = scope
        
        if not update_data:
            print("更新する内容が指定されていません")
            return False
        
        try:
            response = requests.patch(url, headers=self.headers, json=update_data)
            response.raise_for_status()
            print("記事の更新に成功しました！")
            return True
        except requests.exceptions.RequestException as e:
            print(f"記事の更新に失敗しました: {e}")
            if hasattr(e.response, 'text'):
                print(f"エラー詳細: {e.response.text}")
            return False
    
    def show_post_info(self, post_id: int):
        """
        記事の現在の情報を表示
        
        Args:
            post_id: 記事のID
        """
        post = self.get_post(post_id)
        if post:
            print("=== 現在の記事情報 ===")
            print(f"タイトル: {post.get('title', 'N/A')}")
            print(f"作成日: {post.get('created_at', 'N/A')}")
            print(f"更新日: {post.get('updated_at', 'N/A')}")
            print(f"タグ: {', '.join([tag['name'] for tag in post.get('tags', [])])}")
            print(f"公開範囲: {post.get('scope', 'N/A')}")
            print(f"本文の文字数: {len(post.get('body', ''))}")
            print("=" * 30)
        else:
            print("記事の取得に失敗しました")

def main():
    """メイン関数 - 使用例"""
    
    # 環境変数から設定を読み込む
    TEAM_NAME = os.getenv("DOCBASE_TEAM", "go")  # チーム名
    POST_ID = int(os.getenv("DOCBASE_ARTICLE_ID", "2705590"))  # 記事ID
    ACCESS_TOKEN = os.getenv("DOCBASE_API_TOKEN")  # APIトークン
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_API_TOKEN が設定されていません")
        print("\n以下の方法で設定してください：")
        print("1. .envファイルをコピーして設定:")
        print("   cp .env.example .env")
        print("   # .envファイルを編集してAPIトークンを設定")
        print("\n2. または環境変数を直接設定:")
        print("   export DOCBASE_API_TOKEN='あなたのアクセストークン'")
        return
    
    # DocBaseクライアントを作成
    client = DocBaseUpdater(TEAM_NAME, ACCESS_TOKEN)
    
    # 現在の記事情報を表示
    print(f"記事ID {POST_ID} の情報を取得中...")
    client.show_post_info(POST_ID)
    
    # 更新確認
    print("\n記事を更新しますか？")
    print("1. タイトルのみ更新")
    print("2. 本文のみ更新") 
    print("3. タイトルと本文を更新")
    print("4. キャンセル")
    
    choice = input("選択してください (1-4): ")
    
    if choice == "1":
        new_title = input("新しいタイトルを入力してください: ")
        client.update_post(POST_ID, title=new_title)
    elif choice == "2":
        print("新しい本文を入力してください（Ctrl+Dで終了）:")
        new_body = ""
        try:
            while True:
                line = input()
                new_body += line + "\n"
        except EOFError:
            pass
        client.update_post(POST_ID, body=new_body.rstrip())
    elif choice == "3":
        new_title = input("新しいタイトルを入力してください: ")
        print("新しい本文を入力してください（Ctrl+Dで終了）:")
        new_body = ""
        try:
            while True:
                line = input()
                new_body += line + "\n"
        except EOFError:
            pass
        client.update_post(POST_ID, title=new_title, body=new_body.rstrip())
    else:
        print("更新をキャンセルしました")

if __name__ == "__main__":
    main()