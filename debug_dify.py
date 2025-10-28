#!/usr/bin/env python3
"""
Dify APIの詳細デバッグ用スクリプト
"""

import os
import requests
import json
import uuid
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

def debug_dify_api():
    """Dify APIの詳細デバッグ"""
    print("=== Dify API 詳細デバッグ ===")
    
    api_key = os.getenv('DIFY_API_KEY')
    api_url = os.getenv('DIFY_API_URL')
    
    print(f"API Key: {api_key[:20]}..." if api_key else "API Key: 未設定")
    print(f"API URL: {api_url}")
    
    if not api_key or not api_url:
        print("❌ 設定が不完全です")
        return
    
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
    
    print(f"送信データ: {json.dumps(data, indent=2, ensure_ascii=False)}")
    print(f"ヘッダー: {json.dumps(headers, indent=2, ensure_ascii=False)}")
    
    try:
        print("\nAPI呼び出し中...")
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        
        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンスヘッダー: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 成功: {result}")
        else:
            print(f"❌ エラー: {response.status_code}")
            print(f"エラー内容: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ リクエストエラー: {e}")
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")

if __name__ == '__main__':
    debug_dify_api()
