#!/usr/bin/env python3
import json
import re

def load_json(filename):
    """JSONファイルを読み込む"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_faqs_from_body(body):
    """本文からFAQを抽出"""
    faqs = []
    lines = body.splitlines()
    
    current_q = None
    current_a = []
    in_answer = False
    
    for line in lines:
        # 質問の開始
        if line.startswith('#### Q:'):
            # 前の質問がある場合は保存
            if current_q and current_a:
                faqs.append({
                    'question': current_q,
                    'answer': '\n'.join(current_a).strip()
                })
            
            current_q = line[7:].strip()
            current_a = []
            in_answer = False
        
        # 回答の開始
        elif line.startswith('**A:**') or (current_q and line.startswith('- [ ]') and 'Web反映対象' in line):
            in_answer = True
            if line.startswith('**A:**'):
                current_a.append(line)
        
        # 回答の続き
        elif in_answer and current_q:
            # 次の質問や見出しが来たら終了
            if line.startswith('#') or line.startswith('---'):
                in_answer = False
            else:
                current_a.append(line)
    
    # 最後の質問を保存
    if current_q and current_a:
        faqs.append({
            'question': current_q,
            'answer': '\n'.join(current_a).strip()
        })
    
    return faqs

def compare_faqs():
    """FAQの比較を行う"""
    print("データを読み込み中...")
    backup_data = load_json('article_backup.json')
    current_data = load_json('current_article.json')
    
    backup_body = backup_data.get('body', '')
    current_body = current_data.get('body', '')
    
    # FAQを抽出
    print("\nFAQを抽出中...")
    backup_faqs = extract_faqs_from_body(backup_body)
    current_faqs = extract_faqs_from_body(current_body)
    
    print(f"バックアップのFAQ数: {len(backup_faqs)}")
    print(f"現在のFAQ数: {len(current_faqs)}")
    
    # 現在の質問リストを作成
    current_questions = {faq['question'] for faq in current_faqs}
    
    # 削除されたFAQを特定
    deleted_faqs = []
    for faq in backup_faqs:
        if faq['question'] not in current_questions:
            deleted_faqs.append(faq)
    
    print(f"\n削除されたFAQ数: {len(deleted_faqs)}")
    
    # 削除されたFAQを保存
    with open('deleted_faqs.json', 'w', encoding='utf-8') as f:
        json.dump(deleted_faqs, f, ensure_ascii=False, indent=2)
    
    # 削除されたFAQをMarkdown形式で保存
    with open('deleted_faqs.md', 'w', encoding='utf-8') as f:
        f.write("# 削除されたFAQ一覧\n\n")
        f.write(f"削除されたFAQ数: {len(deleted_faqs)}\n\n")
        
        for i, faq in enumerate(deleted_faqs, 1):
            f.write(f"## {i}. {faq['question']}\n")
            f.write(f"{faq['answer']}\n\n")
            f.write("---\n\n")
    
    # 削除されたFAQの概要を表示
    print("\n=== 削除されたFAQの例 ===")
    for i, faq in enumerate(deleted_faqs[:10], 1):  # 最初の10個を表示
        print(f"{i}. Q: {faq['question']}")
        answer_preview = faq['answer'].replace('\n', ' ')[:100]
        print(f"   A: {answer_preview}...")
        print()
    
    if len(deleted_faqs) > 10:
        print(f"... 他 {len(deleted_faqs) - 10} 件\n")
    
    print("削除されたFAQを以下のファイルに保存しました:")
    print("  - deleted_faqs.json (JSON形式)")
    print("  - deleted_faqs.md (Markdown形式)")

if __name__ == "__main__":
    compare_faqs()