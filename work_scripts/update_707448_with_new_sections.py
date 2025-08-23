#!/usr/bin/env python3
"""
記事707448にPowerArQ FP600セクションを追加し、ソーラーパネルセクションを再構成するスクリプト
"""

import json

# 既存の記事内容を読み込む
with open('/Users/g.ohorudingusu/Docbase/article_707448_backup.json', 'r', encoding='utf-8') as f:
    article = json.load(f)

current_body = article.get('body', '')

# 1. PowerArQ FP600セクションを追加
# PowerArQ S10 Proについてのセクションを探す
s10_pro_position = current_body.find("## 🔌 PowerArQ S10 Proについて")

if s10_pro_position == -1:
    print("PowerArQ S10 Proセクションが見つかりませんでした。別の場所を探します。")
    # PowerArQ Maxの後に追加
    max_position = current_body.find("## 🔌 PowerArQ Maxについて")
    if max_position != -1:
        # PowerArQ Maxセクションの終わりを探す
        next_section = current_body.find("\r\n## ", max_position + 1)
        if next_section != -1:
            insertion_point = next_section
        else:
            insertion_point = len(current_body)
    else:
        print("適切な挿入位置が見つかりませんでした")
        insertion_point = -1
else:
    # S10 Proセクションの終わりを探す
    next_section = current_body.find("\r\n## ", s10_pro_position + 1)
    if next_section != -1:
        insertion_point = next_section
    else:
        # ソーラーパネルセクションを探す
        solar_position = current_body.find("## ☀️ PowerArQ Solar（ソーラーパネル）について")
        if solar_position != -1:
            insertion_point = solar_position - 2  # 改行を考慮
        else:
            insertion_point = len(current_body)

# PowerArQ FP600セクションを作成
fp600_section = """\r\n\r\n## 🔌 PowerArQ FP600について\r\n\r\n<details>\r\n<summary>クリックして展開</summary>\r\n\r\n<!-- PowerArQ FP600に関するFAQをここに追加 -->\r\n\r\n</details>"""

# FP600セクションを挿入
if insertion_point != -1:
    new_body = current_body[:insertion_point] + fp600_section + current_body[insertion_point:]
    print("PowerArQ FP600セクションを追加しました")
else:
    new_body = current_body
    print("PowerArQ FP600セクションの追加位置が見つかりませんでした")

# 2. ソーラーパネルセクションを再構成
# 既存の「PowerArQ Solar（ソーラーパネル）について」を「PowerArQ Solar（ソーラーパネル）全般について」に変更
new_body = new_body.replace("## ☀️ PowerArQ Solar（ソーラーパネル）について", 
                           "## ☀️ PowerArQ Solar（ソーラーパネル）全般について")

# ソーラーパネルセクションの終わりを探す
solar_general_position = new_body.find("## ☀️ PowerArQ Solar（ソーラーパネル）全般について")
if solar_general_position != -1:
    # 次のセクション（電気一般に関する質問）を探す
    electric_position = new_body.find("## ⚡ 電気一般に関する質問", solar_general_position)
    if electric_position != -1:
        solar_insertion_point = electric_position - 2  # 改行を考慮
    else:
        solar_insertion_point = len(new_body)
    
    # 新しいソーラーパネルセクションを作成
    pasl120_section = """\r\n\r\n## ☀️ PASL120FD-MC4DCについて\r\n\r\n<details>\r\n<summary>クリックして展開</summary>\r\n\r\n<!-- PASL120FD-MC4DCに関するFAQをここに追加 -->\r\n\r\n</details>"""
    
    pasl210_section = """\r\n\r\n## ☀️ PASL210FD-MC4DCについて\r\n\r\n<details>\r\n<summary>クリックして展開</summary>\r\n\r\n<!-- PASL210FD-MC4DCに関するFAQをここに追加 -->\r\n\r\n</details>"""
    
    # セクションを挿入
    new_body = new_body[:solar_insertion_point] + pasl120_section + pasl210_section + new_body[solar_insertion_point:]
    print("PASL120FD-MC4DCとPASL210FD-MC4DCセクションを追加しました")
else:
    print("ソーラーパネルセクションが見つかりませんでした")

# 新しい内容を保存
with open('/Users/g.ohorudingusu/Docbase/formatted_post_content_707448.md', 'w', encoding='utf-8') as f:
    f.write(new_body)

print("\nセクションの追加と再構成が完了しました。")
print("formatted_post_content_707448.md に保存しました。")