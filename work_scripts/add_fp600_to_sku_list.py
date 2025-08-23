#!/usr/bin/env python3
"""
記事1276088にPowerArQ FP600を追加するスクリプト
"""

import json

# 既存の記事内容を読み込む
with open('/Users/g.ohorudingusu/Docbase/article_1276088_backup.json', 'r', encoding='utf-8') as f:
    article = json.load(f)

current_body = article.get('body', '')

# PowerArQ S10 Proセクションの後にPowerArQ FP600を追加
# S10 Proのテーブルを探す
s10_pro_section = "| <span style=\"font-size:150%;\">**PowerArQ S10 Pro**</span> |  |  |  |"

# テーブルの終了位置を探す（次のセクションの開始位置）
insertion_point = current_body.find(s10_pro_section)
if insertion_point == -1:
    print("PowerArQ S10 Proセクションが見つかりませんでした")
    exit(1)

# S10 Proのテーブル行の終了位置を探す
start_search = insertion_point
lines = current_body[start_search:].split('\r\n')

# S10 Proのテーブルが何行あるか数える
table_end_index = 0
for i, line in enumerate(lines):
    if i > 0 and line.strip() and not line.strip().startswith('|'):
        table_end_index = i
        break
    elif i > 0 and line.strip().startswith('| <span style="font-size:'):
        table_end_index = i
        break

# 実際の挿入位置を計算
actual_lines = current_body.split('\r\n')
s10_pro_line_index = 0
for i, line in enumerate(actual_lines):
    if s10_pro_section in line:
        s10_pro_line_index = i
        break

# PowerArQ FP600のセクションを作成
fp600_section = """| <span style="font-size:150%;">**PowerArQ FP600**</span> |  |  |  |
|  | コヨーテタン | A0055 |  |"""

# 新しい内容を作成
new_lines = actual_lines[:s10_pro_line_index + table_end_index] + fp600_section.split('\r\n') + actual_lines[s10_pro_line_index + table_end_index:]
new_body = '\r\n'.join(new_lines)

# 新しい内容を保存
with open('/Users/g.ohorudingusu/Docbase/formatted_post_content_1276088.md', 'w', encoding='utf-8') as f:
    f.write(new_body)

print("PowerArQ FP600セクションを追加しました。")
print("formatted_post_content_1276088.md に保存しました。")