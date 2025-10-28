#!/usr/bin/env python3
"""
ローカル環境でのテスト用スクリプト
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

def test_dify_api():
    """Dify APIのテスト"""
    print("=== Dify API テスト ===")
    
    api_key = os.getenv('DIFY_API_KEY')
    api_url = os.getenv('DIFY_API_URL')
    
    if not api_key or not api_url:
        print("❌ Dify API設定が不完全です")
        print("DIFY_API_KEY と DIFY_API_URL を設定してください")
        return False
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'inputs': {},
        'query': 'こんにちは、テストメッセージです',
        'response_mode': 'blocking',
        'user': 'test_user'
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        answer = result.get('answer', '')
        
        if answer:
            print(f"✅ Dify API応答成功: {answer[:100]}...")
            return True
        else:
            print("❌ Dify APIから空の応答を受信")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Dify API呼び出しエラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False

def test_line_config():
    """LINE設定のテスト"""
    print("\n=== LINE設定テスト ===")
    
    access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    channel_secret = os.getenv('LINE_CHANNEL_SECRET')
    
    if not access_token or not channel_secret:
        print("❌ LINE設定が不完全です")
        print("LINE_CHANNEL_ACCESS_TOKEN と LINE_CHANNEL_SECRET を設定してください")
        return False
    
    # トークンの形式チェック
    if not access_token.startswith('Bearer ') and len(access_token) > 100:
        print("✅ LINE Channel Access Token形式OK")
    else:
        print("⚠️  LINE Channel Access Tokenの形式を確認してください")
    
    if len(channel_secret) > 20:
        print("✅ LINE Channel Secret形式OK")
    else:
        print("⚠️  LINE Channel Secretの形式を確認してください")
    
    return True

def test_flask_app():
    """Flaskアプリのテスト"""
    print("\n=== Flaskアプリテスト ===")
    
    try:
        # ローカルサーバーが起動しているかチェック
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ Flaskアプリが起動しています")
            return True
        else:
            print(f"❌ Flaskアプリの応答エラー: {response.status_code}")
            return False
    except requests.exceptions.RequestException:
        print("❌ Flaskアプリが起動していません")
        print("python app.py でアプリを起動してください")
        return False

def main():
    """メインテスト実行"""
    print("LINE Chatbot with Dify - ローカルテスト")
    print("=" * 50)
    
    # 環境変数ファイルの存在チェック
    if not os.path.exists('.env'):
        print("❌ .envファイルが見つかりません")
        print("env_example.txtを参考に.envファイルを作成してください")
        print("詳細は env_setup_guide.md を参照してください")
        return
    
    print("✅ .envファイルが見つかりました")
    
    # 各テストを実行
    dify_ok = test_dify_api()
    line_ok = test_line_config()
    flask_ok = test_flask_app()
    
    print("\n" + "=" * 50)
    print("テスト結果:")
    print(f"Dify API: {'✅ OK' if dify_ok else '❌ NG'}")
    print(f"LINE設定: {'✅ OK' if line_ok else '❌ NG'}")
    print(f"Flaskアプリ: {'✅ OK' if flask_ok else '❌ NG'}")
    
    if dify_ok and line_ok and flask_ok:
        print("\n🎉 すべてのテストが成功しました！")
        print("Renderにデプロイする準備ができています。")
    else:
        print("\n⚠️  一部のテストが失敗しました。")
        print("設定を確認してから再実行してください。")

if __name__ == '__main__':
    main()
