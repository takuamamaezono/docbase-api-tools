#!/usr/bin/env python3
"""
「電気一般に関する質問」セクションの内容を分析して
商品固有の質問を特定する
"""

import requests
import json
import os
import re
from dotenv import load_dotenv

load_dotenv()

def get_article(team_name, access_token, post_id):
    """記事内容を取得"""
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/teams/{team_name}/posts/{post_id}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"記事の取得に失敗しました: {e}")
        return None

def extract_electric_section_faqs(body):
    """電気一般セクションのFAQを抽出"""
    
    # 電気一般セクションを特定
    electric_pattern = r'## ⚡ 電気一般に関する質問.*?</details>'
    electric_match = re.search(electric_pattern, body, re.DOTALL)
    
    if not electric_match:
        print("⚠️ 電気一般セクションが見つかりません")
        return []
    
    electric_content = electric_match.group(0)
    
    # FAQを抽出
    faq_pattern = r'#### Q:\s*([^\n\r]+).*?- \[ \] Web反映対象.*?\*\*A:\*\*\s*([^#]*?)(?=####|</details>|$)'
    faqs = re.findall(faq_pattern, electric_content, re.DOTALL)
    
    analyzed_faqs = []
    
    for question, answer in faqs:
        question = question.strip()
        answer = answer.strip()
        
        # 商品名を検出
        product_keywords = {
            'PowerArQ': ['PowerArQ', 'powerarq'],
            'PowerArQ2': ['PowerArQ2', 'powerarq2'],
            'PowerArQ3': ['PowerArQ3', 'powerarq3'],
            'PowerArQ Pro': ['PowerArQ Pro', 'powerarq pro'],
            'PowerArQ mini': ['PowerArQ mini', 'powerarq mini'],
            'PowerArQ mini2': ['PowerArQ mini2', 'powerarq mini2'],
            'PowerArQ S7': ['PowerArQ S7', 'powerarq s7', 'S7'],
            'PowerArQ Max': ['PowerArQ Max', 'powerarq max'],
            'PowerArQ S10': ['PowerArQ S10', 'powerarq s10', 'S10'],
            'Solar': ['Solar', 'solar', 'ソーラー'],
        }
        
        detected_products = []
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        for product, keywords in product_keywords.items():
            for keyword in keywords:
                if keyword.lower() in question_lower or keyword.lower() in answer_lower:
                    detected_products.append(product)
                    break
        
        # 一般的な電気用語かどうかを判定
        general_keywords = [
            'AC', 'DC', 'アンペア', 'ボルト', 'ワット', 'バッテリーセル', 'PSE', 
            '電圧', '電流', '周波数', '交流', '直流', '電気', '充電', 'W数',
            'mAh', 'Wh', '定格', '容量', '出力', '入力'
        ]
        
        is_general = any(keyword in question or keyword in answer for keyword in general_keywords)
        is_product_specific = len(detected_products) > 0
        
        # 分類を決定
        if is_product_specific:
            category = f"商品固有 ({', '.join(set(detected_products))})"
        elif is_general:
            category = "電気一般"
        else:
            category = "要確認"
        
        analyzed_faqs.append({
            'question': question,
            'answer': answer,
            'category': category,
            'detected_products': list(set(detected_products)),
            'is_general': is_general,
            'is_product_specific': is_product_specific
        })
    
    return analyzed_faqs

def main():
    TEAM_NAME = "go"
    POST_ID = 707448
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🔍 電気一般セクションの質問分析")
    print("=" * 50)
    
    # 記事を取得
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 電気一般セクションのFAQを分析
    faqs = extract_electric_section_faqs(body)
    
    if not faqs:
        print("⚠️ FAQが見つかりませんでした")
        return
    
    print(f"📊 分析結果: {len(faqs)}個のFAQを発見")
    print()
    
    # カテゴリ別に分類
    categories = {}
    for faq in faqs:
        category = faq['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(faq)
    
    # 結果を表示
    for category, faq_list in categories.items():
        print(f"📋 【{category}】: {len(faq_list)}個")
        
        for i, faq in enumerate(faq_list, 1):
            print(f"   {i}. Q: {faq['question'][:60]}...")
            if faq['detected_products']:
                print(f"      → 検出商品: {', '.join(faq['detected_products'])}")
        print()
    
    # 移動が必要な質問をまとめ
    product_specific_faqs = [faq for faq in faqs if faq['is_product_specific']]
    
    if product_specific_faqs:
        print(f"🔄 移動が必要な質問: {len(product_specific_faqs)}個")
        print()
        
        # 商品別にグループ化
        product_groups = {}
        for faq in product_specific_faqs:
            for product in faq['detected_products']:
                if product not in product_groups:
                    product_groups[product] = []
                product_groups[product].append(faq)
        
        print("📦 商品別移動先:")
        for product, faq_list in product_groups.items():
            print(f"   {product}: {len(faq_list)}個の質問")
            for faq in faq_list:
                print(f"     • {faq['question'][:50]}...")
        
        # 移動計画をファイルに保存
        move_plan = {
            'total_faqs': len(faqs),
            'general_faqs': len([f for f in faqs if not f['is_product_specific']]),
            'product_specific_faqs': len(product_specific_faqs),
            'product_groups': product_groups,
            'faqs_to_move': product_specific_faqs
        }
        
        with open('faq_move_plan.json', 'w', encoding='utf-8') as f:
            json.dump(move_plan, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 移動計画を faq_move_plan.json に保存しました")
        print(f"")
        print(f"🚀 次のステップ:")
        print(f"   1. 移動計画を確認")
        print(f"   2. 商品固有質問を適切なセクションに移動")
        print(f"   3. 電気一般セクションを整理")
    
    else:
        print("✅ すべての質問が適切に分類されています")

if __name__ == "__main__":
    main()