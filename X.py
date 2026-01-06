#!/usr/bin/env python3
"""
X APIを使用してXに投稿するスクリプト
"""

import os
import sys
from dotenv import load_dotenv
import tweepy
import argparse

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
        print("README.mdを参考に.envファイルを作成してください。")
        sys.exit(1)

    return {
        'api_key': api_key,
        'api_secret': api_secret,
        'access_token': access_token,
        'access_token_secret': access_token_secret,
        'bearer_token': bearer_token
    }


def post_tweet(text, debug=False):
    """Xに任意の文字列を投稿"""
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

        # デバッグモード: 送信されるテキストの詳細を表示
        if debug:
            print("=" * 50)
            print("デバッグ情報: 送信されるテキスト")
            print("=" * 50)
            print(repr(text))  # repr()で改行やスペースを可視化
            print("=" * 50)
            print("テキストの各行:")
            for i, line in enumerate(text.split('\n'), 1):
                print(f"行{i}: {repr(line)}")
            print("=" * 50)
            print(f"文字数: {len(text)}")
            print(f"行数: {len(text.splitlines())}")
            print("=" * 50)

        # 投稿を実行
        print(f"投稿中: {text}")
        response = client.create_tweet(text=text)

        if response.data:
            tweet_id = response.data['id']
            print(f"✅ 投稿成功！")
            print(f"ツイートID: {tweet_id}")
            print(f"URL: https://x.com/i/web/status/{tweet_id}")
            return True
        else:
            print("❌ 投稿に失敗しました。")
            return False

    except tweepy.TooManyRequests as e:
        print("❌ レート制限に達しました。しばらく待ってから再試行してください。")
        if debug:
            print(f"詳細: {e}")
        return False
    except tweepy.Unauthorized as e:
        print("❌ 認証に失敗しました。APIキーとトークンを確認してください。")
        if debug:
            print(f"詳細: {e}")
            print("\n確認事項:")
            print("  - .envファイルに正しい認証情報が設定されているか")
            print("  - APIキー、APIシークレット、アクセストークン、アクセストークンシークレットが正しいか")
        return False
    except tweepy.Forbidden as e:
        print("❌ アクセスが拒否されました。アプリの権限設定を確認してください。")
        if debug:
            print(f"詳細: {e}")
            print(f"エラーレスポンス: {e.response}")
        print("\n確認事項:")
        print("  1. https://developer.x.com でアプリの設定を確認")
        print("  2. App permissions が 'Read and Write' または 'Read and write and Direct message' になっているか")
        print("  3. OAuth 1.0a が有効になっているか")
        print("  4. アクセストークンとアクセストークンシークレットが正しく設定されているか")
        print("  5. アカウントが凍結されていないか、制限されていないか")
        return False
    except tweepy.BadRequest as e:
        print("❌ リクエストが不正です。")
        if debug:
            print(f"詳細: {e}")
            print(f"エラーレスポンス: {e.response}")
        return False
    except Exception as e:
        print(f"❌ エラーが発生しました: {type(e).__name__}: {e}")
        if debug:
            import traceback
            print("\nトレースバック:")
            traceback.print_exc()
        return False


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description='X APIを使用してXに投稿するスクリプト',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')
    
    # postコマンド
    post_parser = subparsers.add_parser('post', help='任意の文字列を投稿する')
    post_parser.add_argument('text', nargs='*', help='投稿するテキスト')
    post_parser.add_argument('-f', '--file', type=str, help='ファイルからテキストを読み込む（アスキーアートなどに便利）')
    post_parser.add_argument('-i', '--stdin', action='store_true', help='標準入力からテキストを読み込む')
    post_parser.add_argument('-d', '--debug', action='store_true', help='デバッグモード: 送信されるテキストの詳細を表示')
    
    args = parser.parse_args()
    
    if args.command == 'post':
        text = None
        
        # 標準入力から読み込む
        if args.stdin:
            text = sys.stdin.read()
        # ファイルから読み込む
        elif args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    text = f.read()
            except FileNotFoundError:
                print(f"❌ エラー: ファイル '{args.file}' が見つかりません。")
                sys.exit(1)
            except Exception as e:
                print(f"❌ ファイル読み込みエラー: {e}")
                sys.exit(1)
        # コマンドライン引数から読み込む
        elif args.text:
            text = ' '.join(args.text)
        else:
            post_parser.print_help()
            sys.exit(1)
        
        # テキストが空でないことを確認
        if not text or not text.strip():
            print("❌ エラー: 投稿するテキストが空です。")
            sys.exit(1)
        
        # 改行文字をそのまま保持（アスキーアート用）
        # 注意: Xは先頭と末尾の空白を自動的に削除する可能性があります
        post_tweet(text.rstrip(), debug=args.debug)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

