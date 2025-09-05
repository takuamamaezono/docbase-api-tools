#!/usr/bin/env python3
"""
PowerArQ FP600のSKUをA0055に修正するスクリプト
"""

import json

# 最新の記事内容を読み込む
with open('/Users/g.ohorudingusu/Docbase/article_664151_backup.json', 'r', encoding='utf-8') as f:
    article = json.load(f)

current_body = article.get('body', '')

# PowerArQ FP600のSKUを修正
new_body = current_body.replace('| 2025年月 | 未定 | 200 | CFST001 | 初回納品 |', 
                                 '| 2025年月 | A0055 | 200 | CFST001 | 初回納品 |')

# 新しい内容を保存
with open('/Users/g.ohorudingusu/Docbase/formatted_post_content.md', 'w', encoding='utf-8') as f:
    f.write(new_body)

print("PowerArQ FP600のSKUをA0055に修正しました。")