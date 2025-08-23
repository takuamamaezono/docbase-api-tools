#!/usr/bin/env python3
"""
記事707448にPowerArQ FP600セクションを追加し、ソーラーパネルセクションを再構成するスクリプト
"""

import json
import re

# 既存の記事内容を読み込む
with open('/Users/g.ohorudingusu/Docbase/article_707448_backup.json', 'r', encoding='utf-8') as f:
    article = json.load(f)

current_body = article.get('body', '')

# 1. PowerArQ S10 Proの後にPowerArQ FP600セクションを追加
# S10 Proセクションを探す
s10_pro_pattern = r'(## 🔌 PowerArQ S10 Pro について\s*<details open>.*?</details>)'
match = re.search(s10_pro_pattern, current_body, re.DOTALL)

if match:
    s10_pro_end = match.end()
    
    # PowerArQ FP600セクションを作成
    fp600_section = '\n\n## 🔌 PowerArQ FP600について\n<details open>\n<summary>詳細はこちら</summary>\n\n<!-- PowerArQ FP600に関するFAQをここに追加 -->\n\n</details>'
    
    # S10 Proの後に挿入
    new_body = current_body[:s10_pro_end] + fp600_section + current_body[s10_pro_end:]
else:
    print("PowerArQ S10 Proセクションが見つかりませんでした")
    new_body = current_body

# 2. ソーラーパネルセクションを再構成
# 既存の「PowerArQ Solar（ソーラーパネル）について」を「PowerArQ Solar（ソーラーパネル）全般について」に変更
new_body = new_body.replace('## ☀️ PowerArQ Solar（ソーラーパネル）について', 
                           '## ☀️ PowerArQ Solar（ソーラーパネル）全般について')

# ソーラーパネルセクションの終わりを探す
solar_pattern = r'(## ☀️ PowerArQ Solar（ソーラーパネル）全般について\s*<details open>.*?</details>)'
solar_match = re.search(solar_pattern, new_body, re.DOTALL)

if solar_match:
    solar_end = solar_match.end()
    
    # 新しいソーラーパネルセクションを作成
    pasl120_section = '\n\n## ☀️ PASL120FD-MC4DCについて\n<details open>\n<summary>詳細はこちら</summary>\n\n<!-- PASL120FD-MC4DCに関するFAQをここに追加 -->\n\n</details>'
    pasl210_section = '\n\n## ☀️ PASL210FD-MC4DCについて\n<details open>\n<summary>詳細はこちら</summary>\n\n<!-- PASL210FD-MC4DCに関するFAQをここに追加 -->\n\n</details>'
    
    # ソーラーパネル全般の後に挿入
    new_body = new_body[:solar_end] + pasl120_section + pasl210_section + new_body[solar_end:]
else:
    print("ソーラーパネルセクションが見つかりませんでした")

# 新しい内容を保存
with open('/Users/g.ohorudingusu/Docbase/formatted_post_content_707448.md', 'w', encoding='utf-8') as f:
    f.write(new_body)

print("セクションの追加と再構成が完了しました。")
print("- PowerArQ FP600セクションを追加")
print("- ソーラーパネルセクションを「全般について」に変更")
print("- PASL120FD-MC4DCセクションを追加")
print("- PASL210FD-MC4DCセクションを追加")
print("formatted_post_content_707448.md に保存しました。")