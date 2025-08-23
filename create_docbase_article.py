#!/usr/bin/env python3
"""
Docbaseに新しい記事を作成するスクリプト
"""
import requests
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

# .envファイルから設定を読み込む
TEAM_NAME = os.getenv("DOCBASE_TEAM", "go")
ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")

# --- ここに作成したい記事の内容を記述 ---

# 記事のタイトル
ARTICLE_TITLE = "Docbase FAQ更新ツールの仕様"

# 記事の本文（Markdown形式）
ARTICLE_BODY = """
# Docbase FAQ更新ツールの仕様調査レポート

## 1. 概要
このドキュメントは、`/Users/g.ohorudingusu/Docbase/` に格納されているFAQ管理および更新ツール群の仕様を調査した結果をまとめたものです。

## 2. 主要なツールと役割

### 2.1. `docbase_helper.sh`
- **役割**: 日常的な記事の取得、更新、セクション追加などを簡単に行うためのラッパーツール。
- **特徴**: 記事IDを引数に取り、簡単なコマンドでDocbaseの記事を操作できる。

### 2.2. `faq_tools/` ディレクトリ
- **役割**: FAQ記事���管理に特化したツール群が格納されている。
- **主要なスクリリプト**:
    - `faq_flag_manager.py`: FAQのWeb公開フラグを管理する対話型ツール。
    - `web_sync_filter.py` (※言及のみ): Web公開対象のFAQを抽出・整形するツール。

## 3. FAQ更新のコア機能：Web公開フラグ

FAQの更新は、各質問項目に付けられたチェックボックス形式の「フラグ」によって制御されます。

- `- [ ] Web反映対象`: このFAQはWebサイトに**公開する**。
- `- [x] Web反映除外`: このFAQはWebサイトに**公開しない**。

このフラグにより、社内限定の情報やテスト中の項目をWebサイトの更新から除外することができます。

## 4. `faq_flag_manager.py` の詳細仕様

- **目的**: 特定の記事（ID: `2705590`）内のFAQフラグを効率的に管理する。
- **機能**:
    1.  **フラグ状況の分析**: 記事全体のフラグ状況（対象、除外、フラグ無し）を集計・表示する。
    2.  **全FAQへのフラグ追加**: フラグが未設定のFAQに対し、デフォルトで「Web反映対象」フラグを一括で追加する。
    3.  **個別フラグの切り替え**: セクション名と質問内容の一部を指定して、特定のFAQのフラグを対話��式で変更する。
    4.  **記事の更新**: スクリプト内で行った変更をDocbaseに反映する。
- **重要な注意点**:
    - **対象記事がハードコードされている**: チーム名 `go` と記事ID `2705590` がスクリプト内に直接記述されているため、他の記事には使用できません。
    - **対話型インターフェース**: コマンドライン上でメニューを選択して操作します。

## 5. 全体のワークフロー

1.  **フラグ管理 (`faq_flag_manager.py`)**:
    - 社内でのみ閲覧したいFAQや、まだ公開したくないFAQに「Web反映除外」フラグを設定する。
2.  **データ抽出 (`web_sync_filter.py`)**:
    - 「Web反映対象」のフラグが付いたFAQのみを抽出し、Webサイト連携用のデータ（JSON, HTML等）を生成する。
3.  **Webサイト更新**:
    - 抽出されたデータを利用して、WebサイトのFAQページを更新する。

## 6. まとめ
- FAQ更新システムは、**特定の記事**を対象に、**マークダウンのチェックボックス**を利用してWeb公開範囲を制御する仕組みです。
- `faq_flag_manager.py` はそのフラグをメンテナンスするための便利なツールですが、**汎用的なものではなく、特定記事専用**である点���注意が必要です。
"""

# -----------------------------------------

def create_docbase_article(team_name, access_token, title, body):
    """
    Docbaseに新しい記事を作成する
    """
    base_url = "https://api.docbase.io"
    url = f"{base_url}/teams/{team_name}/posts"
    
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    # DOCBASE_RULES.md に従い、公開範囲を private に設定
    payload = {
        "title": title,
        "body": body,
        "draft": False,
        "scope": "private",  # 従業員のみに公開
        "tags": ["FAQ", "仕様", "ツール"]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        created_post = response.json()
        print("✅ 記事の作成に成功しました！")
        print(f"   記事ID: {created_post['id']}")
        print(f"   タイトル: {created_post['title']}")
        print(f"   URL: {created_post['url']}")
        return created_post
        
    except requests.exceptions.RequestException as e:
        print(f"❌ 記事の作成に失敗しました: {e}")
        if e.response:
            print(f"   ステータスコード: {e.response.status_code}")
            print(f"   レスポンス: {e.response.text}")
        return None

if __name__ == "__main__":
    if not ACCESS_TOKEN:
        print("❌ 環境変数 `DOCBASE_ACCESS_TOKEN` が設定されていません。")
        print("   `.env` ファイルを確認してください。")
    else:
        print("🚀 Docbaseに新しい記事を作成します...")
        create_docbase_article(TEAM_NAME, ACCESS_TOKEN, ARTICLE_TITLE, ARTICLE_BODY)
