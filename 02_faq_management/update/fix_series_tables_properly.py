#!/usr/bin/env python3
"""
PowerArQ全シリーズの表形式情報を正確に追加する
ユーザーが提供した内容をそのまま正確に反映
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

def remove_broken_series_info(body):
    """壊れた全シリーズ情報を削除"""
    
    print("🧹 既存の壊れた情報を削除中...")
    
    # 削除するパターンのリスト
    patterns_to_remove = [
        # 壊れたシガーソケット情報
        r'#### Q: PowerArQ 全シリーズ　シガーソケットの出力最大電力\(瞬間\)について.*?(?=#### Q:|</details>|$)',
        # 壊れたファン情報
        r'#### Q: PowerArQ 全シリーズ　ファンの動作条件について.*?(?=#### Q:|</details>|$)',
        # 壊れた出力W数情報
        r'#### Q: PowerArQ 全シリーズ　出力のW数の表示について.*?(?=#### Q:|</details>|$)',
        # 壊れた自動停止情報
        r'#### Q: PowerArQ 全シリーズ　自動で出力が停止する条件.*?(?=#### Q:|</details>|$)',
        r'#### Q: 各PowerArQシリーズ 自動で出力が停止する条件.*?(?=#### Q:|</details>|$)',
        # 壊れたACアダプター情報
        r'#### Q: ▼各PowerArQシリーズ　ACアダプターのランプの色.*?(?=#### Q:|</details>|$)',
        # その他の断片的な情報
        r'#### Q: 製品名\s*- \[ \] Web反映対象.*?(?=#### Q:|</details>|$)',
        r'#### Q: PowerArQ（Hモード）\s*- \[ \] Web反映対象.*?(?=#### Q:|</details>|$)',
        r'#### Q: PowerArQ626Wh Mk1\s*- \[ \] Web反映対象.*?(?=#### Q:|</details>|$)',
        r'# PowerArQ 全シリーズ　ファンの動作条件について.*?(?=#### Q:|</details>|$)'
    ]
    
    cleaned_body = body
    removed_count = 0
    
    for pattern in patterns_to_remove:
        matches = re.findall(pattern, cleaned_body, re.DOTALL)
        if matches:
            removed_count += len(matches)
            cleaned_body = re.sub(pattern, '', cleaned_body, flags=re.DOTALL)
    
    # 余分な改行を整理
    cleaned_body = re.sub(r'\n{4,}', '\n\n', cleaned_body)
    
    print(f"   ✅ {removed_count}個の壊れた情報を削除しました")
    
    return cleaned_body

def add_correct_series_info(body):
    """正しい全シリーズ情報を追加"""
    
    print("📝 正しい全シリーズ情報を追加中...")
    
    # ユーザーが提供した正確な内容
    correct_series_info = """

#### Q: PowerArQ 全シリーズ　シガーソケットの出力最大電力(瞬間)について
- [ ] Web反映対象
**A:** 
| 製品名 | 最大電力(シガーソケット部) | 
| --- | --- | 
| PowerArQ | 最大電流(A)/電圧(V)：約13A/12V<br>最大電力：約156W | 
| PowerArQPro | 最大電流(A)/電圧(V)：約11A/12V<br>最大電力：約132W | 
| PowerArQmini | 最大電流(A)/電圧(V)：約15A/12V<br>最大電力：約180W | 
| PowerArQ2, mini2, PowerArQ3 | 最大電流(A)/電圧(V)：約13.5A/12V<br>最大電力：約162W | 
| PowerArQ S10 Pro | 最大電流(A)/電圧(V)：約10A/14.4V<br>最大電力：約144W |

#### Q: PowerArQ 全シリーズ　ファンの動作条件について
- [ ] Web反映対象
**A:** 
| 製品名 | ファンの動作条件 | 
| --- | --- | 
| PowerArQ, PowerArQ mini, PowerArQ Pro, PowerArQ mini2 | ・内部温度が45度以上 | 
| PowerArQ2 | ・内部温度が50度以上<br>・出力70W以上 | 
| PowerArQ3 | ・AC出力200W以上<br>・DC出力100W以上<br>・温度が60℃以上 | 
| PowerArQ MAX | ・AC出力1000W以上<br>・DC出力150W以上<br>・内部のヒートシンクの温度が50℃以上 |
| PowerArQ S10 Pro | ・AC出力50W以上<br>・DC出力50W以上<br>・AC、DC同時出力50W以上<br>・内部のヒートシンクの温度が45℃以上 |
| PowerArQ S7 | ・AC出力300W以上<br>・DC出力95W以上<br>・入力90W以上<br>・エラー「TEMP」が表示された時<br>※S7は内部温度での自動動作はありません。|

▼PowerArQ2に関しては以下もご覧ください。
[PowerArQ2 仕様変更記録](https://go.docbase.io/posts/664151#powerarq-2)

#### Q: PowerArQ 全シリーズ　出力のW数の表示について
- [ ] Web反映対象
**A:** 
| 製品名 | AC出力のW数　表示の仕様 | 
| --- | --- | 
| PowerArQ, PowerArQ mini, PowerArQ Pro | DC出力：±5W<br>AC出力：±20W(10w以下の場合0~10Wと表示される場合がある) | 
| PowerArQ2, PowerArQ3, PowerArQmini2 | DC出力：±5W<br>AC出力：±20W(10W以下の場合0Wと表示される)<br><br>▼Max<br>DC出力：±5W<br>AC出力：±30W(20W以下の場合0Wと表示される) | 
| PowerArQ S7 | ワイヤレス：±3W<br>AC：±30W<br>DC：±6W<br><span style="color:#d70910;">※S7のみ、ワイヤレス別</span> |
| PowerArQ Max | AC：±30W<br>DC：±10W | 
| PowerArQ S10 Pro | AC出力：±5%(出力約20W以下、0W表示可能)<br>USBA：±2W(出力約2W以下、0W表示可能)<br>USBC/シガー：±5W(出力約5W以下、0W表示可能) | 

※出力0Wと表示されていても、接続機器への給電が止まっていなければ仕様です。

#### Q: PowerArQ 全シリーズ　自動で出力が停止する条件
- [ ] Web反映対象
**A:** 基本的には「PowerArQ、PowerArQ mini、PowerArQ pro、PowerArQ3」は手動電源オフモードの時は<span style="color: #afb5bb">（PowerArQ3はECOモードという名前）</span>手動で出力を停止しないと出力は停止しません。
「PowerArQ2、PowerArQ mini2」も機器を接続して出力状態の時は、手動で出力を停止しないと出力は停止しません。

ですが、手動電源OFFモードでも出力W数が小さい場合、PowerArQが「出力している」と認識せず、自動で出力状態をOFFにしてしまいます。（出力状態にしていても、機器を接続して出力されていなければ、一定の時間が経過すると出力が停止します。）

#### Q: ▼各PowerArQシリーズ 自動で出力が停止する条件
- [ ] Web反映対象
**A:** 
|  | AC出力 | USB出力 | DC出力 | 自動で停止する時間 |
| --- | --- | --- | --- | --- |
| PowerArQ（Hモード） | 10W以下 | 約140mA以下（電圧５Vで計算すると、約0.7W） | 10W以下 | 約6~12時間 |
| PowerArQ mini（Hモード） | 10W以下 | 約140mA以下（電圧５Vで計算すると、約0.7W） | 10W以下 | 約3時間 |
| PowerArQ pro（Hモード） | 10W以下 | 約140mA以下（電圧５Vで計算すると、約0.7W） | 10W以下 | 約12時間 |
| PowerArQ2 | 制限なし | 制限なし | 制限なし | 制限なしのため、出力は止まらない |
| PowerArQ mini2 | 制限なし | 制限なし | 制限なし | 制限なしのため、出力は止まらない |
| PowerArQ3（ECOモード） | 30W以下 | 5W以下 | 5W以下 | 約4時間 |
| PowerArQ3（Hモード） | 制限なし | 制限なし | 制限なし | 制限なしのため、出力は止まらない |
| PowerArQ Max（ECOモード） | 30W以下 | 制限なし | 制限なし | 約4時間 |
| PowerArQ Max（Hモード） | 制限なし | 制限なし | 制限なし | 制限なしのため、出力は止まらない |
| PowerArQ S7（ECOモード） | AC出力10W以下 | 制限なし | 制限なし | 約4時間 |
| PowerArQ S10 Pro（ECOモード） | 50W以下で2時間経過するとOFFになる | USB Type-A：出力1W以下で2時間経過するとOFFになる<br>USB Type-C：出力2W以下で2時間経過するとOFFになる | 5W以下で12時間経過するとOFFになる | それぞれの欄に記載 |
| PowerArQ S10 Pro（Hモード） | 制限なし | 制限なし | 制限なし | 制限なしのため、出力は止まらない |

#### Q: ▼各PowerArQシリーズ　ACアダプターのランプの色
- [ ] Web反映対象
**A:** 
| 製品名 | ACアダプターのランプの色 |
| --- | --- |
| PowerArQ626Wh Mk1 | <span style="color: #00CC00">緑点灯</span> |
| PowerArQ626Wh Mk2(旧、新含め) | <span style="color: red">赤点灯</span> |
| PowerArQ626Wh Mk3 | <span style="color: red">赤点灯</span> |
| PowerArQ mini Mk1 | <span style="color: #00CC00">緑点灯</span> |
| PowerArQ mini Mk2 | <span style="color: red">赤点灯</span> |
| PowerArQ2 | <span style="color: red">赤点灯</span> |
| PowerArQ pro | <span style="color: red">赤点灯</span> |
| PowerArQ mini 2 | <span style="color: red">赤点灯</span> |
| PowerArQ3 | <span style="color: red">赤点灯</span> |
| PowerArQ S7 | <span style="color: red">赤点灯</span> |
| PowerArQ MAX | <span style="color: red">赤点灯</span> |"""
    
    # PowerArQシリーズ全般セクションを探す
    general_pattern = r'(## 🔋 PowerArQシリーズ全般 について\s*\n\s*<details>\s*\n\s*<summary>.*?</summary>\s*\n)(.*?)(</details>)'
    general_match = re.search(general_pattern, body, re.DOTALL)
    
    if not general_match:
        print("⚠️ PowerArQシリーズ全般セクションが見つかりません")
        return body
    
    # 既存のセクション内容を取得
    section_prefix = general_match.group(1)
    existing_content = general_match.group(2)
    section_suffix = general_match.group(3)
    
    # 新しい内容を追加（既存の内容の最後に追加）
    new_content = existing_content.rstrip() + correct_series_info + "\n"
    
    # セクションを再構築
    new_section = section_prefix + new_content + section_suffix
    
    # 記事を更新
    updated_body = body.replace(general_match.group(0), new_section)
    
    print("✅ 以下の情報を正確に追加しました:")
    print("   • PowerArQ 全シリーズ　シガーソケットの出力最大電力(瞬間)について")
    print("   • PowerArQ 全シリーズ　ファンの動作条件について")
    print("   • PowerArQ 全シリーズ　出力のW数の表示について")
    print("   • PowerArQ 全シリーズ　自動で出力が停止する条件")
    print("   • ▼各PowerArQシリーズ 自動で出力が停止する条件（詳細表）")
    print("   • ▼各PowerArQシリーズ　ACアダプターのランプの色")
    
    return updated_body

def update_article(team_name, access_token, post_id, updated_body):
    """記事を更新"""
    base_url = "https://api.docbase.io"
    headers = {
        "X-DocBaseToken": access_token,
        "Content-Type": "application/json"
    }
    
    url = f"{base_url}/teams/{team_name}/posts/{post_id}"
    update_data = {"body": updated_body}
    
    try:
        response = requests.patch(url, headers=headers, json=update_data)
        response.raise_for_status()
        print("✅ 記事の更新に成功しました！")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ 記事の更新に失敗しました: {e}")
        return False

def main():
    TEAM_NAME = "go"
    POST_ID = 707448
    ACCESS_TOKEN = os.getenv("DOCBASE_ACCESS_TOKEN")
    
    if not ACCESS_TOKEN:
        print("環境変数 DOCBASE_ACCESS_TOKEN が設定されていません")
        return
    
    print("🔧 PowerArQ全シリーズ情報修正システム")
    print("=" * 60)
    print("• 壊れた情報を削除")
    print("• 正しい全シリーズ情報を追加")
    print("=" * 60)
    
    # 記事を取得
    print("📄 記事を取得中...")
    article_data = get_article(TEAM_NAME, ACCESS_TOKEN, POST_ID)
    
    if not article_data:
        return
    
    body = article_data['body']
    
    # 処理前のFAQ数
    before_faq_count = len(re.findall(r'#### Q:', body))
    print(f"📊 処理前のFAQ数: {before_faq_count}個")
    
    # 1. 壊れた情報を削除
    cleaned_body = remove_broken_series_info(body)
    
    # 2. 正しい情報を追加
    updated_body = add_correct_series_info(cleaned_body)
    
    # 処理後のFAQ数
    after_faq_count = len(re.findall(r'#### Q:', updated_body))
    print(f"📊 処理後のFAQ数: {after_faq_count}個")
    
    if updated_body != body:
        print(f"\n🔄 記事を更新中...")
        success = update_article(TEAM_NAME, ACCESS_TOKEN, POST_ID, updated_body)
        
        if success:
            print(f"\n🎉 全シリーズ情報の修正完了！")
            print(f"")
            print(f"📱 修正内容:")
            print(f"   • 壊れた情報を削除")
            print(f"   • ユーザー提供の正確な内容を追加")
            print(f"   • PowerArQシリーズ全般セクションに適切に配置")
            print(f"")
            print(f"💡 確認:")
            print(f"   https://go.docbase.io/posts/{POST_ID}")
    else:
        print(f"\n✅ 更新の必要はありませんでした")

if __name__ == "__main__":
    main()