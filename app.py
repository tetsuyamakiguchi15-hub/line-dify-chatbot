from flask import Flask, request, jsonify
import os
import requests
import json
import uuid
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import logging

# .envファイルを読み込み
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 環境変数から設定を取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
DIFY_API_KEY = os.getenv('DIFY_API_KEY')
DIFY_API_URL = os.getenv('DIFY_API_URL')

# LINE Bot API の初期化
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def call_dify_api(user_message, user_id):
    """
    Dify APIを呼び出してAI応答を取得
    """
    try:
        # 環境変数の確認
        if not DIFY_API_KEY or not DIFY_API_URL:
            logger.error("Dify API設定が不完全です")
            return "設定エラーが発生しました。管理者にお問い合わせください。"
        
        headers = {
            'Authorization': f'Bearer {DIFY_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'inputs': {},
            'query': user_message,
            'response_mode': 'blocking',
            'user': user_id
        }
        
        logger.info(f"Dify API呼び出し: {user_message[:50]}...")
        
        response = requests.post(
            DIFY_API_URL, 
            headers=headers, 
            json=data,
            timeout=30  # 30秒のタイムアウト
        )
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Dify API応答取得成功")
        
        # 応答の取得と検証
        answer = result.get('answer', '')
        if not answer:
            logger.warning("Dify APIから空の応答を受信")
            return "申し訳ございません。現在応答を生成できませんでした。"
        
        # 応答が長すぎる場合は切り詰め
        if len(answer) > 2000:
            answer = answer[:2000] + "..."
            logger.info("応答を2000文字に切り詰めました")
        
        return answer
        
    except requests.exceptions.Timeout:
        logger.error("Dify API呼び出しがタイムアウトしました")
        return "申し訳ございません。応答に時間がかかりすぎています。しばらくしてからもう一度お試しください。"
    except requests.exceptions.RequestException as e:
        logger.error(f"Dify API呼び出しエラー: {e}")
        return "申し訳ございません。現在サービスが利用できません。"
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析エラー: {e}")
        return "申し訳ございません。応答の処理中にエラーが発生しました。"
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        return "申し訳ございません。エラーが発生しました。"

@app.route('/')
def home():
    return "LINE Chatbot with Dify is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    LINEからのWebhookを受信
    """
    # リクエストの署名を検証
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    
    # 環境変数の確認
    if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
        logger.error("LINE Bot設定が不完全です")
        return jsonify({'error': 'Configuration error'}), 500
    
    try:
        handler.handle(body, signature)
        logger.info("Webhook処理成功")
    except InvalidSignatureError:
        logger.error("Invalid signature. Please check your channel secret.")
        return jsonify({'error': 'Invalid signature'}), 400
    except Exception as e:
        logger.error(f"Webhook処理エラー: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return jsonify({'status': 'success'})

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    テキストメッセージを処理
    """
    try:
        user_message = event.message.text
        user_id = event.source.user_id
        
        logger.info(f"Received message from {user_id}: {user_message}")
        
        # メッセージの長さチェック
        if len(user_message) > 500:
            logger.warning(f"メッセージが長すぎます: {len(user_message)}文字")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="申し訳ございません。メッセージが長すぎます。500文字以内でお送りください。")
            )
            return
        
        # Dify APIを呼び出してAI応答を取得
        ai_response = call_dify_api(user_message, user_id)
        
        # LINEに応答を送信
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ai_response)
        )
        
        logger.info(f"応答送信完了: {ai_response[:50]}...")
        
    except Exception as e:
        logger.error(f"メッセージ処理エラー: {e}")
        try:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="申し訳ございません。エラーが発生しました。しばらくしてからもう一度お試しください。")
            )
        except Exception as reply_error:
            logger.error(f"エラー応答送信失敗: {reply_error}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
