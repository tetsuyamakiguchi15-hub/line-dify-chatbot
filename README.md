# LINE Chatbot with Dify Integration

LINEとDifyを連携したAIチャットボットです。Renderで無料デプロイできます。

## 機能

- LINEからのメッセージを受信
- Dify APIを使用してAI応答を生成
- LINEにAI応答を送信

## セットアップ手順

### 1. LINE Developers設定

1. [LINE Developers Console](https://developers.line.biz/)にアクセス
2. 新しいプロバイダーを作成
3. チャンネルを作成（Messaging API）
4. 以下の情報を取得：
   - Channel Access Token
   - Channel Secret

### 2. Dify設定

1. [Dify](https://dify.ai/)にアクセス
2. アカウントを作成
3. 新しいアプリを作成
4. APIキーを取得
5. API URLを確認（通常は `https://api.dify.ai/v1/chat-messages`）

### 3. 環境変数設定

#### ローカル開発用
1. プロジェクト直下に`.env`ファイルを作成
2. 以下の内容を記入（実際の値に置き換え）：

```env
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_CHANNEL_SECRET=your_line_channel_secret
DIFY_API_KEY=your_dify_api_key
DIFY_API_URL=https://api.dify.ai/v1/chat-messages
```

**重要**: ファイル名は必ず`.env`にしてください！

詳細は `env_setup_guide.md` を参照してください。

### 4. Renderデプロイ

1. [Render](https://render.com/)にアカウント作成
2. GitHubリポジトリを連携
3. 新しいWebサービスを作成
4. 環境変数を設定
5. デプロイ実行

### 5. LINE Webhook設定

1. LINE Developers ConsoleでWebhook URLを設定
2. URL: `https://your-app-name.onrender.com/webhook`
3. Webhookの使用を有効化

## ローカル開発

```bash
# 依存関係をインストール
pip install -r requirements.txt

# .envファイルを作成（env_example.txtを参考に）
# ファイル名は必ず .env にしてください！

# アプリを実行
python app.py

# テスト実行
python test_local.py
```

## ファイル構成

- `app.py`: メインのFlaskアプリケーション
- `requirements.txt`: Python依存関係
- `render.yaml`: Renderデプロイ設定
- `env_example.txt`: 環境変数の例
