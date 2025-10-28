# 🚀 クイックスタートガイド

## 5分でLINEチャットボットをデプロイ！

### ステップ1: 必要なアカウント作成
1. **LINE Developers** (https://developers.line.biz/)
2. **Dify** (https://dify.ai/)
3. **GitHub** (https://github.com/)
4. **Render** (https://render.com/)

### ステップ2: 設定情報を取得

#### LINE設定
1. LINE Developers Consoleで新しいチャンネルを作成
2. **Channel Access Token** と **Channel Secret** をコピー

#### Dify設定
1. Difyで新しいアプリを作成
2. **API Key** をコピー
3. **API URL** を確認（通常：`https://api.dify.ai/v1/chat-messages`）

### ステップ3: GitHubにアップロード
1. このプロジェクトをGitHubリポジトリにアップロード
2. すべてのファイルが含まれていることを確認

### ステップ4: Renderでデプロイ
1. Renderで新しいWebサービスを作成
2. GitHubリポジトリを選択
3. 環境変数を設定：
   ```
   LINE_CHANNEL_ACCESS_TOKEN = [LINEのトークン]
   LINE_CHANNEL_SECRET = [LINEのシークレット]
   DIFY_API_KEY = [DifyのAPIキー]
   DIFY_API_URL = https://api.dify.ai/v1/chat-messages
   ```
4. デプロイ実行

### ステップ5: LINE Webhook設定
1. LINE Developers ConsoleでWebhook URLを設定
2. URL: `https://your-app-name.onrender.com/webhook`
3. Webhookを有効化

### ステップ6: テスト
1. LINEアプリで友だち追加
2. メッセージを送信
3. AI応答を確認

## 🎉 完了！
これでLINEチャットボットが動作します！

## トラブルシューティング
- エラーが発生した場合は `setup_guide.md` を参照
- ログはRenderダッシュボードで確認可能
