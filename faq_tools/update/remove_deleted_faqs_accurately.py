#!/usr/bin/env python3
import os
import json
import requests
import re
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

def remove_faqs_accurately():
    """削除されたFAQを正確に除外"""
    print("削除されたFAQを正確に除外中...")
    
    # 現在の記事を取得
    url = f'https://api.docbase.io/teams/{TEAM}/posts/{ARTICLE_ID}'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        article_info = response.json()
        
        # 現在の本文（復元された状態）
        current_body = article_info.get('body', '')
        
        print(f"現在の本文長: {len(current_body)} 文字")
        
        # 削除すべきFAQのリスト
        faqs_to_remove = [
            "MC4ケーブルの寸法は？",
            "本体にACアダプタの内蔵は可能ですか？",
            "ACアダプター交換、在庫切れの場合",
            "ACアダプターだけ購入できますか？",
            "ACアダプタが発火する可能性はありますか？",
            "バッテリー有償交換サービスを使用する目安はどのような状態ですか？",
            "カーインバーターから充電可能ですか？",
            "液晶表示がON/OFFでなく数秒で消えるのはどうしてですか？",
            "本体の重さを軽減する事は可能ですか？",
            "本体が雨に打たれた場合、どの程度の水量だと使用不可能になりますか？",
            "本体の近くで火を使用した場合、本体または内部電池に引火する可能性はありますか？",
            "12V出力ボタンの消灯が遅いのはどうして？",
            "無停電装置として使える？",
            "008601C-JPN-FS seriesの型番の意味は？",
            "古いACアダプターはINPUTが1.5Aなのですが、新しいACアダプターは2.5Aと上がっています。古いACアダプターで電流が弱く充電できないのでしょうか？ またなぜ、新しいACアダプターが出たのでしょうか？",
            "ACアダプターの種類について",
            "リン酸系とマンガン系のリチウムイオン電池のメリットデメリットは？",
            "医療機器に使用可能ですか？",
            "実機の貸出は出来ますか？",
            "SDS（MSDS）が欲しいです",
            "トランシーバーに干渉してAC出力が自動OFFする",
            "パススルー充電できますか？",
            "修理品を返送する際、梱包はどうしたらいいですか？",
            "人気色は？",
            "満充電後のACアダプターと本体のランプはどうなる？",
            "PowerArQ１outputのサイズは？",
            "ピークパワー(400W)の動作叶時間は？",
            "バッテリーメーカーは？",
            "E28とE31について入力電流とはどういう意味ですか？",
            "INPUTのDC外径と内径について知りたいです。",
            "保護キャップについて",
            "バッテリー差込口が閉まりません。",
            "USB-Cの端子が使えません。",
            "単体バッテリーに充電できているかの確認方法は？",
            "エラー：E36でご利用いただけない冷蔵庫",
            "ディスプレイにある電波マークはなんですか？",
            "設定画面にある「AC出力電圧」は設定しないと故障するのか？",
            "再起動の方法は？"
        ]
        
        # 各FAQを削除
        cleaned_body = current_body
        removed_count = 0
        
        for question in faqs_to_remove:
            # より柔軟なパターンマッチング
            # 質問の前後の改行や空白を考慮
            escaped_q = re.escape(question)
            
            # 複数のパターンを試す
            patterns = [
                # 標準的なパターン
                rf'#### Q: {escaped_q}\s*\n- \[ \] Web反映対象\s*\n\*\*A:\*\*[^#]*?(?=\n#### Q:|## |\n---|\Z)',
                # Web反映対象がないパターン
                rf'#### Q: {escaped_q}\s*\n\*\*A:\*\*[^#]*?(?=\n#### Q:|## |\n---|\Z)',
                # 改行が異なるパターン
                rf'#### Q: {escaped_q}[^\n]*\n[^\n]*\n\*\*A:\*\*[^#]*?(?=\n#### Q:|## |\n---|\Z)'
            ]
            
            for pattern in patterns:
                regex = re.compile(pattern, re.DOTALL | re.MULTILINE)
                if regex.search(cleaned_body):
                    cleaned_body = regex.sub('', cleaned_body)
                    removed_count += 1
                    print(f"削除 {removed_count}: {question[:50]}...")
                    break
        
        # 余分な改行を整理
        cleaned_body = re.sub(r'\n{4,}', '\n\n\n', cleaned_body)
        cleaned_body = re.sub(r'\n{3,}(##)', r'\n\n\1', cleaned_body)
        
        print(f"\nクリーン後の本文長: {len(cleaned_body)} 文字")
        print(f"削除されたFAQ数: {removed_count}/{len(faqs_to_remove)}")
        
        # グループ情報を取得
        current_groups = article_info.get('groups', [])
        group_ids = [group['id'] for group in current_groups]
        
        # 更新データを準備
        update_data = {
            'title': article_info.get('title'),
            'body': cleaned_body,
            'notice': True,
            'scope': article_info.get('scope', 'group'),
            'groups': group_ids
        }
        
        # 記事を更新
        print("\n記事を更新中...")
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n✅ 記事を削除済みFAQを除外した状態に更新しました！")
        print(f"更新日時: {result.get('updated_at')}")
        print(f"記事URL: {result.get('url')}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ エラーが発生しました: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"ステータスコード: {e.response.status_code}")
            print(f"エラー内容: {e.response.text}")
        return None

if __name__ == "__main__":
    if not API_TOKEN or not TEAM:
        print("環境変数 DOCBASE_ACCESS_TOKEN と DOCBASE_TEAM を設定してください。")
    else:
        remove_faqs_accurately()