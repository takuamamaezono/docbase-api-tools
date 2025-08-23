#!/usr/bin/env python3
import json
import difflib
from datetime import datetime

def load_json(filename):
    """JSONファイルを読み込む"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_body(data):
    """記事本文を抽出"""
    return data.get('body', '')

def compare_articles():
    """記事の差分を比較"""
    # ファイルの読み込み
    print("ファイルを読み込み中...")
    backup_data = load_json('article_backup.json')
    current_data = load_json('current_article.json')
    
    # 本文の抽出
    backup_body = extract_body(backup_data)
    current_body = extract_body(current_data)
    
    # 基本情報の表示
    print("\n=== 記事情報 ===")
    print(f"記事ID: {backup_data.get('id')}")
    print(f"タイトル: {backup_data.get('title')}")
    print(f"\nバックアップの更新日時: {backup_data.get('updated_at')}")
    print(f"現在の更新日時: {current_data.get('updated_at')}")
    
    # 行単位で比較
    backup_lines = backup_body.splitlines()
    current_lines = current_body.splitlines()
    
    print(f"\nバックアップの行数: {len(backup_lines)}")
    print(f"現在の行数: {len(current_lines)}")
    
    # 差分の生成
    diff = list(difflib.unified_diff(
        backup_lines,
        current_lines,
        fromfile='バックアップ（更新前）',
        tofile='現在（更新後）',
        lineterm='',
        n=3
    ))
    
    # 削除された行と追加された行をカウント
    deleted_lines = []
    added_lines = []
    
    for line in diff:
        if line.startswith('-') and not line.startswith('---'):
            deleted_lines.append(line)
        elif line.startswith('+') and not line.startswith('+++'):
            added_lines.append(line)
    
    print(f"\n削除された行数: {len(deleted_lines)}")
    print(f"追加された行数: {len(added_lines)}")
    
    # 差分をファイルに保存
    with open('article_diff.txt', 'w', encoding='utf-8') as f:
        f.write("=== 記事の差分 ===\n")
        f.write(f"記事ID: {backup_data.get('id')}\n")
        f.write(f"タイトル: {backup_data.get('title')}\n")
        f.write(f"\nバックアップの更新日時: {backup_data.get('updated_at')}\n")
        f.write(f"現在の更新日時: {current_data.get('updated_at')}\n")
        f.write(f"\n削除された行数: {len(deleted_lines)}\n")
        f.write(f"追加された行数: {len(added_lines)}\n")
        f.write("\n" + "="*50 + "\n\n")
        
        for line in diff:
            f.write(line + '\n')
    
    # 削除された重要な内容を抽出
    print("\n=== 削除された主な内容 ===")
    with open('deleted_content.txt', 'w', encoding='utf-8') as f:
        f.write("=== 削除された内容 ===\n\n")
        for line in deleted_lines:
            content = line[1:].strip()  # 先頭の'-'を除去
            if content and not content.startswith('#'):  # 空行やヘッダー以外
                f.write(content + '\n')
                if '**A:**' in content or 'Q:' in content:
                    print(f"  {content[:80]}...")
    
    print("\n差分ファイルを作成しました:")
    print("  - article_diff.txt (全体の差分)")
    print("  - deleted_content.txt (削除された内容)")

if __name__ == "__main__":
    compare_articles()