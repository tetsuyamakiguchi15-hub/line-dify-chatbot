# 🔧 環境変数設定ガイド

## .envファイルの作成方法

### 1. プロジェクト直下に.envファイルを作成

プロジェクトのルートディレクトリ（`app.py`と同じ場所）に`.env`ファイルを作成してください。

**ファイル名は必ず `.env` にしてください！**

### 2. .envファイルの内容

```env
# LINE Bot設定
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here
LINE_CHANNEL_SECRET=your_line_channel_secret_here

# Dify設定
DIFY_API_KEY=your_dify_api_key_here
DIFY_API_URL=https://api.dify.ai/v1/chat-messages
```

### 3. 実際の値に置き換え

上記の`your_xxx_here`の部分を実際の値に置き換えてください：

```env
# 例（実際の値）
LINE_CHANNEL_ACCESS_TOKEN=Bearer 1234567890abcdefghijklmnopqrstuvwxyz
LINE_CHANNEL_SECRET=abcdef1234567890abcdef1234567890
DIFY_API_KEY=app-1234567890abcdefghijklmnopqrstuvwxyz
DIFY_API_URL=https://api.dify.ai/v1/chat-messages
```

## 環境変数の読み込み方法

### 標準的な方法（推奨）

```python
from dotenv import load_dotenv
import os

# .envファイルを読み込み
load_dotenv()

# 環境変数としてアクセス
api_key = os.getenv("API_KEY")
secret = os.getenv("API_SECRET")
```

### ファイル名を変更した場合

もし`.env`以外の名前を使いたい場合：

```python
from dotenv import load_dotenv
from pathlib import Path
import os

# 特定のファイルを指定
env_path = Path('.') / '.env.local'
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("API_KEY")
```

## 注意事項

### ✅ やること
- ファイル名は`.env`に統一
- プロジェクト直下に配置
- 実際の値に置き換え

### ❌ やってはいけないこと
- `.env`ファイルをGitにコミット
- ファイル名を`.env`以外にする（混乱の元）
- 実際のAPIキーをコードに直接書く

## トラブルシューティング

### よくある問題

1. **「.envファイルが見つからない」エラー**
   - ファイル名が`.env`になっているか確認
   - プロジェクト直下に配置されているか確認

2. **「環境変数がNone」エラー**
   - `.env`ファイルの内容が正しいか確認
   - `load_dotenv()`を呼び出しているか確認

3. **「Permission denied」エラー**
   - ファイルの権限を確認
   - テキストエディタで作成し直す

### 確認方法

```python
# 環境変数が正しく読み込まれているか確認
from dotenv import load_dotenv
import os

load_dotenv()

print("LINE_CHANNEL_ACCESS_TOKEN:", os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
print("DIFY_API_KEY:", os.getenv("DIFY_API_KEY"))
```

## デプロイ時の注意

### Renderデプロイ時
- `.env`ファイルは使用しません
- Renderの環境変数設定で値を設定します

### ローカル開発時
- `.env`ファイルを使用します
- `python-dotenv`ライブラリが必要です

## セキュリティ

- `.env`ファイルには機密情報が含まれます
- 絶対にGitにコミットしないでください
- `.gitignore`に`.env`が含まれていることを確認してください
