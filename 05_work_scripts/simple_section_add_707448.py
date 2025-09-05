#!/usr/bin/env python3
"""
記事707448にPowerArQ FP600と新しいソーラーパネルセクションを追加するスクリプト
"""

import json

# 既存の記事内容を読み込む
with open('/Users/g.ohorudingusu/Docbase/article_707448_backup.json', 'r', encoding='utf-8') as f:
    article = json.load(f)

current_body = article.get('body', '')

# ソーラーパネルについての表記を変更
new_body = current_body.replace("## ☀️ PowerArQ Solar（ソーラーパネル）について", 
                                "## ☀️ PowerArQ Solar（ソーラーパネル）全般について")

# 記事の最後に新しいセクションを追加
additional_sections = """

## 🔌 PowerArQ FP600について

<details>
<summary>クリックして展開</summary>

<!-- PowerArQ FP600に関するFAQをここに追加 -->

</details>

## ☀️ PASL120FD-MC4DCについて

<details>
<summary>クリックして展開</summary>

<!-- PASL120FD-MC4DCに関するFAQをここに追加 -->

</details>

## ☀️ PASL210FD-MC4DCについて

<details>
<summary>クリックして展開</summary>

<!-- PASL210FD-MC4DCに関するFAQをここに追加 -->

</details>"""

# 記事の最後に追加
final_body = new_body + additional_sections

# 新しい内容を保存
with open('/Users/g.ohorudingusu/Docbase/formatted_post_content_707448.md', 'w', encoding='utf-8') as f:
    f.write(final_body)

print("✅ セクションの追加が完了しました：")
print("- PowerArQ Solar（ソーラーパネル）について → PowerArQ Solar（ソーラーパネル）全般について に変更")
print("- PowerArQ FP600についてセクションを追加")
print("- PASL120FD-MC4DCについてセクションを追加") 
print("- PASL210FD-MC4DCについてセクションを追加")
print("formatted_post_content_707448.md に保存しました。")