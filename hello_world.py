#!/usr/bin/env python3
"""
X APIを使用してXに「Hello World」を投稿するスクリプト
"""

import os
import sys
from dotenv import load_dotenv
import tweepy

# .envファイルから環境変数を読み込む
load_dotenv()


def get_api_credentials():
    """環境変数からAPI認証情報を取得"""
    api_key = os.getenv('X_API_KEY')
    api_secret = os.getenv('X_API_SECRET')
    access_token = os.getenv('X_ACCESS_TOKEN')
    access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
    bearer_token = os.getenv('X_BEARER_TOKEN')

    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("エラー: .envファイルに必要な認証情報が設定されていません。")
        print(".env.exampleを参考に.envファイルを作成してください。")
        sys.exit(1)

    return {
        'api_key': api_key,
        'api_secret': api_secret,
        'access_token': access_token,
        'access_token_secret': access_token_secret,
        'bearer_token': bearer_token
    }


def post_hello_world():
    """Xに「Hello World」を投稿"""
    try:
        # 認証情報を取得
        credentials = get_api_credentials()

        # Tweepyクライアントを作成
        client = tweepy.Client(
            bearer_token=credentials['bearer_token'],
            consumer_key=credentials['api_key'],
            consumer_secret=credentials['api_secret'],
            access_token=credentials['access_token'],
            access_token_secret=credentials['access_token_secret'],
            wait_on_rate_limit=True
        )

        # 投稿内容
        tweet_text = "Hello World"

        # 投稿を実行
        print(f"投稿中: {tweet_text}")
        response = client.create_tweet(text=tweet_text)

        if response.data:
            tweet_id = response.data['id']
            print(f"✅ 投稿成功！")
            print(f"ツイートID: {tweet_id}")
            print(f"URL: https://x.com/i/web/status/{tweet_id}")
            return True
        else:
            print("❌ 投稿に失敗しました。")
            return False

    except tweepy.TooManyRequests:
        print("❌ レート制限に達しました。しばらく待ってから再試行してください。")
        return False
    except tweepy.Unauthorized:
        print("❌ 認証に失敗しました。APIキーとトークンを確認してください。")
        return False
    except tweepy.Forbidden:
        print("❌ アクセスが拒否されました。アプリの権限設定を確認してください。")
        return False
    except Exception as e:
        print(f"❌ エラーが発生しました: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    post_hello_world()

