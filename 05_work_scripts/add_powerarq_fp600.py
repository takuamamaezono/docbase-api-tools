#!/usr/bin/env python3
"""
記事664151にPowerArQ FP600のセクションを追加するスクリプト
"""

import json

# 既存の記事内容を読み込む
with open('/Users/g.ohorudingusu/Docbase/article_664151_backup.json', 'r', encoding='utf-8') as f:
    article = json.load(f)

current_body = article.get('body', '')

# PowerArQ S10 Proセクションの後にPowerArQ FP600を追加
# S10 Proセクションを探す
s10_pro_section = "## ■PowerArQ S10 Pro"
insertion_point = current_body.find(s10_pro_section)

if insertion_point == -1:
    print("PowerArQ S10 Proセクションが見つかりませんでした")
    exit(1)

# S10 Proセクションの終わりを探す（次のセクションの開始または本文の終わり）
start_search = insertion_point + len(s10_pro_section)
next_section_start = current_body.find("\r\n\r\n\r\n", start_search)

if next_section_start == -1:
    # 次のセクションが見つからない場合、ポータブル電源の備考セクションを探す
    next_section_start = current_body.find("### ポータブル電源の備考", start_search)
    
if next_section_start == -1:
    # それでも見つからない場合は最後に追加
    next_section_start = len(current_body)

# PowerArQ FP600のセクションを作成
fp600_section = """

## ■PowerArQ FP600
| 日付 | SKU | 納品数量 | ロットNo. | 備考 |
| --- | --- | --- | --- | --- |
| 2025年月 | 未定 | 200 | CFST001 | 初回納品 |"""

# 新しい本文を作成
new_body = current_body[:next_section_start] + fp600_section + current_body[next_section_start:]

# 新しい内容を保存
with open('/Users/g.ohorudingusu/Docbase/formatted_post_content.md', 'w', encoding='utf-8') as f:
    f.write(new_body)

print("PowerArQ FP600セクションを追加しました。")
print("formatted_post_content.md に保存しました。")