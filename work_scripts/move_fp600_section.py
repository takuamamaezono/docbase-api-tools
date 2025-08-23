#!/usr/bin/env python3
"""
記事707448のPowerArQ FP600セクションをソーラーパネル全般の前に移動するスクリプト
"""

# フォーマット済みの内容を読み込む
with open('/Users/g.ohorudingusu/Docbase/formatted_post_content_707448.md', 'r', encoding='utf-8') as f:
    current_body = f.read()

# PowerArQ FP600セクションを削除
fp600_section_start = current_body.find("## 🔌 PowerArQ FP600について")
fp600_section_end = current_body.find("## ☀️ PASL120FD-MC4DCについて")

if fp600_section_start != -1 and fp600_section_end != -1:
    # FP600セクションを取得
    fp600_section = current_body[fp600_section_start:fp600_section_end]
    
    # FP600セクションを削除
    body_without_fp600 = current_body[:fp600_section_start] + current_body[fp600_section_end:]
    
    # ソーラーパネル全般セクションの位置を探す
    solar_general_position = body_without_fp600.find("## ☀️ PowerArQ Solar（ソーラーパネル）全般について")
    
    if solar_general_position != -1:
        # ソーラーパネル全般の前にFP600セクションを挿入
        new_body = body_without_fp600[:solar_general_position] + fp600_section + body_without_fp600[solar_general_position:]
        
        # 新しい内容を保存
        with open('/Users/g.ohorudingusu/Docbase/formatted_post_content_707448.md', 'w', encoding='utf-8') as f:
            f.write(new_body)
        
        print("✅ PowerArQ FP600セクションをソーラーパネル全般セクションの前に移動しました")
    else:
        print("❌ ソーラーパネル全般セクションが見つかりませんでした")
else:
    print("❌ PowerArQ FP600セクションまたはPASL120FD-MC4DCセクションが見つかりませんでした")