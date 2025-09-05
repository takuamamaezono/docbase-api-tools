#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Docbase汎用ヘルパースクリプト
記事の取得、更新、セクション追加などの基本操作を簡単に実行できます
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

# .envファイルから環境変数を読み込み
load_dotenv()

class DocbaseHelper:
    def __init__(self):
        self.api_token = os.getenv('DOCBASE_ACCESS_TOKEN') or os.getenv('DOCBASE_API_TOKEN')
        self.team = os.getenv('DOCBASE_TEAM', 'go')
        
        if not self.api_token:
            print("❌ エラー: DOCBASE_ACCESS_TOKENが設定されていません")
            print("💡 .envファイルにDOCBASE_ACCESS_TOKEN=your_token_hereを追加してください")
            sys.exit(1)
        
        self.headers = {
            'X-DocBaseToken': self.api_token,
            'Content-Type': 'application/json'
        }
        
    def get_article(self, article_id):
        """記事を取得"""
        url = f"https://api.docbase.io/teams/{self.team}/posts/{article_id}"
        
        print(f"📖 記事ID {article_id} を取得中...")
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            article = response.json()
            
            # バックアップファイルに保存
            backup_file = f"article_{article_id}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(article, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 記事を取得しました")
            print(f"📁 バックアップ: {backup_file}")
            print(f"📄 タイトル: {article['title']}")
            print(f"🔗 URL: {article['url']}")
            return article
        else:
            print(f"❌ 記事の取得に失敗しました: {response.status_code}")
            print(response.text)
            return None
    
    def update_article(self, article_id, body=None, title=None):
        """記事を更新"""
        # 現在の記事を取得
        article = self.get_article(article_id)
        if not article:
            return False
        
        # 更新データを準備（bodyのみ更新、tagsは絶対に送信しない）
        update_data = {
            'body': body or article['body']
        }
        
        # タイトルが明示的に指定された場合のみ追加
        if title is not None:
            update_data['title'] = title
        
        # 注意: scope、groups、tagsは一切送信しない（Docbase APIが自動保持する）
        
        # 更新実行
        url = f"https://api.docbase.io/teams/{self.team}/posts/{article_id}"
        print(f"📝 記事ID {article_id} を更新中...")
        
        response = requests.patch(url, headers=self.headers, json=update_data)
        
        if response.status_code == 200:
            print(f"✅ 記事を更新しました")
            print(f"🔗 URL: https://go.docbase.io/posts/{article_id}")
            return True
        else:
            print(f"❌ 更新に失敗しました: {response.status_code}")
            print(response.text)
            return False
    
    def add_section_to_article(self, article_id, section_title, section_content, position='end'):
        """記事にセクションを追加"""
        article = self.get_article(article_id)
        if not article:
            return False
        
        current_body = article['body']
        
        # 新しいセクションを作成
        new_section = f"\n\n## {section_title}\n\n{section_content}"
        
        # 位置に応じて追加
        if position == 'end':
            updated_body = current_body + new_section
        elif position == 'start':
            updated_body = new_section + "\n\n" + current_body
        else:
            # 特定の位置に挿入する場合はここで処理
            updated_body = current_body + new_section
        
        return self.update_article(article_id, body=updated_body)
    
    def replace_section(self, article_id, old_section, new_section):
        """記事の特定セクションを置換"""
        article = self.get_article(article_id)
        if not article:
            return False
        
        current_body = article['body']
        
        # Windows改行コード（\r\n）を考慮した置換
        # まず、old_sectionに\r\nが含まれていない場合、追加して試す
        if '\r\n' not in old_section and '\r\n' in current_body:
            old_section = old_section.replace('\n', '\r\n')
            new_section = new_section.replace('\n', '\r\n')
        
        if old_section not in current_body:
            print("⚠️  指定されたセクションが見つかりません")
            return False
        
        updated_body = current_body.replace(old_section, new_section)
        return self.update_article(article_id, body=updated_body)
    
    def list_articles(self, q=None, per_page=20):
        """記事一覧を取得"""
        url = f"https://api.docbase.io/teams/{self.team}/posts"
        params = {'per_page': per_page}
        if q:
            params['q'] = q
        
        print("📚 記事一覧を取得中...")
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            articles = response.json()['posts']
            print(f"\n📋 記事一覧 ({len(articles)}件):")
            print("-" * 60)
            for article in articles:
                print(f"ID: {article['id']:8} | {article['title'][:40]}")
            return articles
        else:
            print(f"❌ 記事一覧の取得に失敗しました: {response.status_code}")
            return None
    
    def get_all_tags(self):
        """既存のタグ一覧を取得"""
        url = f"https://api.docbase.io/teams/{self.team}/tags"
        
        print("🏷️ 既存タグを取得中...")
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            tags = response.json()
            print(f"✅ {len(tags)} 件のタグを取得しました")
            return tags
        else:
            print(f"❌ タグ一覧の取得に失敗しました: {response.status_code}")
            return None
    
    def display_tags(self, tags):
        """タグ一覧を見やすく表示"""
        if not tags:
            print("❌ 表示するタグがありません")
            return
        
        print("\n🏷️ 利用可能なタグ:")
        print("-" * 60)
        for i, tag in enumerate(tags, 1):
            # posts_countが無い場合は表示しない
            if 'posts_count' in tag:
                print(f"{i:3}. {tag['name']} ({tag['posts_count']}件)")
            else:
                print(f"{i:3}. {tag['name']}")
        print("-" * 60)
    
    def select_tags_interactive(self, tags):
        """インタラクティブなタグ選択"""
        if not tags:
            return []
        
        self.display_tags(tags)
        
        print("\n📝 タグ選択:")
        print("• 番号をカンマ区切りで入力してください (例: 1,3,5)")
        print("• Enterキーのみで選択せずに続行")
        
        try:
            user_input = input("\n選択する番号: ").strip()
            if not user_input:
                return []
            
            # 番号をパース
            selected_indices = []
            for num_str in user_input.split(','):
                try:
                    num = int(num_str.strip())
                    if 1 <= num <= len(tags):
                        selected_indices.append(num - 1)
                    else:
                        print(f"⚠️ 無効な番号: {num}")
                except ValueError:
                    print(f"⚠️ 無効な入力: {num_str}")
            
            # 選択されたタグを取得
            selected_tags = [tags[i]['name'] for i in selected_indices]
            
            if selected_tags:
                print(f"✅ 選択されたタグ: {', '.join(selected_tags)}")
            else:
                print("ℹ️ タグは選択されませんでした")
            
            return selected_tags
            
        except KeyboardInterrupt:
            print("\n❌ 操作がキャンセルされました")
            return []
    
    def create_article(self, title, body, tags=None, scope='private', interactive_tags=True):
        """新規記事を作成"""
        url = f"https://api.docbase.io/teams/{self.team}/posts"
        
        # 記事作成データを準備
        article_data = {
            'title': title,
            'body': body,
            'scope': scope  # private = 従業員のみ（G.O / 加島）
        }
        
        # タグの処理
        if interactive_tags and not tags:
            # 既存タグから選択
            all_tags = self.get_all_tags()
            if all_tags:
                selected_tags = self.select_tags_interactive(all_tags)
                if selected_tags:
                    article_data['tags'] = selected_tags
        elif tags:
            # 指定されたタグを使用（既存チェック）
            all_tags = self.get_all_tags()
            if all_tags:
                existing_tag_names = [tag['name'] for tag in all_tags]
                
                if isinstance(tags, str):
                    tags = [tag.strip() for tag in tags.split(',')]
                
                # 既存タグのみを使用
                valid_tags = []
                for tag in tags:
                    if tag in existing_tag_names:
                        valid_tags.append(tag)
                    else:
                        print(f"⚠️ 存在しないタグをスキップ: {tag}")
                
                if valid_tags:
                    article_data['tags'] = valid_tags
                    print(f"✅ 既存タグを適用: {', '.join(valid_tags)}")
                else:
                    print("ℹ️ 有効なタグがありません")
        
        print(f"📝 新規記事「{title}」を作成中...")
        response = requests.post(url, headers=self.headers, json=article_data)
        
        if response.status_code == 201:
            article = response.json()
            article_id = article['id']
            print(f"✅ 記事を作成しました")
            print(f"📄 記事ID: {article_id}")
            print(f"📄 タイトル: {title}")
            print(f"🔗 URL: https://go.docbase.io/posts/{article_id}")
            return article
        else:
            print(f"❌ 記事の作成に失敗しました: {response.status_code}")
            print(response.text)
            return None
    
    def create_article_with_tag_selection(self, title, body, scope='private'):
        """既存タグ選択付きで新規記事を作成"""
        return self.create_article(title, body, scope=scope, interactive_tags=True)

def main():
    """コマンドライン引数を処理"""
    if len(sys.argv) < 2:
        print("使い方:")
        print("  python docbase_helper.py get <記事ID>")
        print("  python docbase_helper.py update <記事ID> <bodyファイル>")
        print("  python docbase_helper.py add-section <記事ID> <セクション名> <内容>")
        print("  python docbase_helper.py replace <記事ID> <old.txt> <new.txt>")
        print("  python docbase_helper.py list [検索キーワード]")
        print("  python docbase_helper.py create <タイトル> <bodyファイル> [タグ1,タグ2]")
        print("  python docbase_helper.py create-interactive <タイトル> <bodyファイル>")
        print("  python docbase_helper.py tags")
        print("  python docbase_helper.py list-tags")
        sys.exit(1)
    
    helper = DocbaseHelper()
    command = sys.argv[1]
    
    if command == 'get' and len(sys.argv) >= 3:
        article_id = sys.argv[2]
        helper.get_article(article_id)
    
    elif command == 'update' and len(sys.argv) >= 4:
        article_id = sys.argv[2]
        body_file = sys.argv[3]
        with open(body_file, 'r', encoding='utf-8') as f:
            body = f.read()
        helper.update_article(article_id, body=body)
    
    elif command == 'add-section' and len(sys.argv) >= 5:
        article_id = sys.argv[2]
        section_title = sys.argv[3]
        section_content = sys.argv[4]
        helper.add_section_to_article(article_id, section_title, section_content)
    
    elif command == 'replace' and len(sys.argv) >= 5:
        article_id = sys.argv[2]
        old_file = sys.argv[3]
        new_file = sys.argv[4]
        with open(old_file, 'r', encoding='utf-8') as f:
            old_section = f.read()
        with open(new_file, 'r', encoding='utf-8') as f:
            new_section = f.read()
        helper.replace_section(article_id, old_section, new_section)
    
    elif command == 'create' and len(sys.argv) >= 4:
        title = sys.argv[2]
        body_file = sys.argv[3]
        tags = sys.argv[4] if len(sys.argv) >= 5 else None
        with open(body_file, 'r', encoding='utf-8') as f:
            body = f.read()
        # 従来方式（既存タグチェック付き）
        helper.create_article(title, body, tags=tags, interactive_tags=False)
    
    elif command == 'create-interactive' and len(sys.argv) >= 4:
        title = sys.argv[2]
        body_file = sys.argv[3]
        with open(body_file, 'r', encoding='utf-8') as f:
            body = f.read()
        # インタラクティブタグ選択
        helper.create_article_with_tag_selection(title, body)
    
    elif command == 'list':
        q = sys.argv[2] if len(sys.argv) >= 3 else None
        helper.list_articles(q=q)
    
    elif command in ['tags', 'list-tags']:
        # タグ一覧を表示
        tags = helper.get_all_tags()
        if tags:
            helper.display_tags(tags)
    
    else:
        print("❌ 無効なコマンドです")
        sys.exit(1)

if __name__ == "__main__":
    main()