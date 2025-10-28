# LINE Chatbot with Dify セットアップガイド

## 必要な準備

### 1. LINE Developers設定

1. **LINE Developers Console**にアクセス
   - https://developers.line.biz/ja/

2. **プロバイダー作成**
   - 「Create」→「Provider」を選択
   - プロバイダー名を入力（例：「My Chatbot Provider」）

3. **チャンネル作成**
   - 「Create」→「Messaging API」を選択
   - チャンネル名を入力（例：「AI Chatbot」）
   - チャンネル説明を入力
   - カテゴリを選択（例：「Business」）
   - 利用規約に同意

4. **必要な情報を取得**
   - **Channel Access Token**（長期）
   - **Channel Secret**

### 2. Dify設定

1. **Difyアカウント作成**
   - https://dify.ai/ にアクセス
   - アカウントを作成

2. **アプリケーション作成**
   - 「Create App」をクリック
   - アプリ名を入力（例：「LINE Chatbot AI」）
   - アプリタイプを選択（「Chatbot」推奨）

3. **API設定**
   - アプリの「API」タブに移動
   - **API Key**をコピー
   - **API URL**を確認（通常：`https://api.dify.ai/v1/chat-messages`）

### 3. GitHubリポジトリ作成

1. **新しいリポジトリ作成**
   - GitHubで新しいリポジトリを作成
   - リポジトリ名（例：「line-dify-chatbot」）

2. **ファイルをアップロード**
   - 作成したファイルをすべてアップロード

### 4. Renderデプロイ

1. **Renderアカウント作成**
   - https://render.com/ にアクセス
   - GitHubアカウントでサインアップ

2. **新しいWebサービス作成**
   - 「New」→「Web Service」を選択
   - GitHubリポジトリを選択
   - 以下の設定を行う：
     - **Name**: `line-dify-chatbot`（任意）
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`

3. **環境変数設定**
   - 「Environment」タブで以下を設定：
     ```
     LINE_CHANNEL_ACCESS_TOKEN = your_line_channel_access_token
     LINE_CHANNEL_SECRET = your_line_channel_secret
     DIFY_API_KEY = your_dify_api_key
     DIFY_API_URL = https://api.dify.ai/v1/chat-messages
     ```

4. **デプロイ実行**
   - 「Create Web Service」をクリック
   - デプロイ完了まで待機（5-10分）

### 5. LINE Webhook設定

1. **LINE Developers Console**に戻る
2. **Messaging API設定**タブを開く
3. **Webhook URL**を設定：
   ```
   https://your-app-name.onrender.com/webhook
   ```
4. **Webhookの利用**を「利用する」に設定
5. **応答メッセージ**を「利用しない」に設定
6. **友だち追加時のあいさつ**を「利用しない」に設定

### 6. 動作確認

1. **LINEアプリで友だち追加**
   - QRコードまたは友だち追加リンクを使用

2. **メッセージ送信テスト**
   - 任意のメッセージを送信
   - AI応答が返ってくることを確認

## トラブルシューティング

### よくある問題

1. **Webhookエラー**
   - URLが正しいか確認
   - HTTPSが使用されているか確認
   - 環境変数が正しく設定されているか確認

2. **Dify APIエラー**
   - APIキーが正しいか確認
   - API URLが正しいか確認
   - Difyアプリが有効になっているか確認

3. **デプロイエラー**
   - requirements.txtの依存関係を確認
   - ログを確認してエラー内容を特定

### ログ確認方法

1. **Renderダッシュボード**
   - サービスの「Logs」タブでログを確認

2. **LINE Developers Console**
   - 「Messaging API設定」→「Webhook送信」で送信状況を確認

## カスタマイズ

### 応答メッセージの変更
- `app.py`の`call_dify_api`関数内のエラーメッセージを変更

### メッセージ長制限の変更
- `app.py`の`handle_message`関数内の文字数制限を変更

### ログレベルの変更
- `app.py`の`logging.basicConfig`でログレベルを変更
