# X

```
┌──(stardust✨stardust)-[~/X]
└─$ pyenv local 3.12.8

┌──(stardust✨stardust)-[~/X]
└─$ exec $SHEL -l

┌──(stardust✨stardust)-[~/X]
└─$ python -V
Python 3.12.8

┌──(stardust✨stardust)-[~/X]
└─$ python -m venv venv

┌──(stardust✨stardust)-[~/X]
└─$ source venv/bin/activate

┌──(venv)(stardust✨stardust)-[~/X]
└─$ python -V
Python 3.12.8
```

# X APIを使用してXにHello Worldを投稿したい。

## セットアップ

### 1. 依存関係のインストール

```bash
┌──(venv)(stardust✨stardust)-[~/X]
└─$ pip install -r requirements.txt
```

### 2. X API認証情報の設定

1. https://developer.x.com でDeveloperアカウントを作成
2. ProjectとAppを作成し、Read/Write権限を設定
3. APIキー、APIシークレット、アクセストークン、アクセストークンシークレット、Bearerトークンを取得
4. `.env`ファイルを作成し、以下の形式で認証情報を設定：

```bash
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_TOKEN_SECRET=your_access_token_secret_here
X_BEARER_TOKEN=your_bearer_token_here
```

### 3. 実行

```bash
┌──(venv)(stardust✨stardust)-[~/X]
└─$ python hello_world.py
投稿中: Hello World
✅ 投稿成功！
ツイートID: 2008603481293418556
URL: https://x.com/i/web/status/2008603481293418556
```

これでXに「Hello World」が投稿されます。

## ファイル構成

- `hello_world.py` - メインの投稿スクリプト
- `requirements.txt` - 必要なPythonパッケージ
- `.gitignore` - Gitで除外するファイル（.envなど）
- `.env` - API認証情報（このファイルはGitにコミットしないでください）

## 注意事項

- `.env`ファイルには機密情報が含まれるため、Gitにコミットしないでください
- X APIの無料ティアでは月500投稿まで可能です
- スパム行為はアカウント凍結の原因となるため、適切な使用を心がけてください
