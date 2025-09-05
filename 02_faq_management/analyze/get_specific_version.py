#!/usr/bin/env python3
import os
import json
import requests
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数の設定
API_TOKEN = os.getenv('DOCBASE_ACCESS_TOKEN')
TEAM = os.getenv('DOCBASE_TEAM')
ARTICLE_ID = '707448'

# ヘッダーの設定
headers = {
    'X-DocBaseToken': API_TOKEN,
    'Content-Type': 'application/json'
}

def get_article_at_time():
    """12:28更新の記事を取得するため、履歴を確認"""
    url = f'https://api.docbase.io/teams/{TEAM}/posts/{ARTICLE_ID}'
    
    print("記事の履歴情報を取得中...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        article_data = response.json()
        
        print(f"記事タイトル: {article_data.get('title', 'タイトルなし')}")
        print(f"最終更新日時: {article_data.get('updated_at', '不明')}")
        print(f"更新者: {article_data.get('user', {}).get('name', '不明')}")
        
        # 履歴APIがない場合、現在の状態から削除されたFAQを除外する必要がある
        # deleted_faqs.jsonから削除されたFAQの情報を読み込む
        with open('deleted_faqs.json', 'r', encoding='utf-8') as f:
            deleted_faqs = json.load(f)
        
        print(f"\n削除すべきFAQ数: {len(deleted_faqs)}")
        
        # 現在の本文を取得
        current_body = article_data.get('body', '')
        
        # 削除されたFAQを本文から取り除く
        cleaned_body = current_body
        for faq in deleted_faqs:
            # 各FAQを本文から削除
            # 質問と回答の全体を削除する必要がある
            question = faq['question']
            answer = faq['answer']
            
            # FAQのパターンを作成（#### Q: から次の#### Q: または見出しまで）
            faq_pattern = f"#### Q: {question}\n- [ ] Web反映対象\n{answer}"
            
            if faq_pattern in cleaned_body:
                cleaned_body = cleaned_body.replace(faq_pattern, '')
                print(f"削除: Q: {question[:50]}...")
        
        # 余分な改行を整理
        cleaned_body = cleaned_body.replace('\n\n\n', '\n\n')
        
        # クリーンな記事を保存
        with open('cleaned_article_body.md', 'w', encoding='utf-8') as f:
            f.write(cleaned_body)
        
        print(f"\nクリーンな記事本文を cleaned_article_body.md に保存しました。")
        print(f"元の文字数: {len(current_body)}")
        print(f"クリーン後の文字数: {len(cleaned_body)}")
        
        return cleaned_body
        
    except requests.exceptions.RequestException as e:
        print(f"エラーが発生しました: {e}")
        return None

if __name__ == "__main__":
    if not API_TOKEN or not TEAM:
        print("環境変数 DOCBASE_ACCESS_TOKEN と DOCBASE_TEAM を設定してください。")
    else:
        get_article_at_time()