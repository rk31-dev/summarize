import sys
import requests
from bs4 import BeautifulSoup
import re

def fetch_content(url):
    """指定されたURLのコンテンツを取得し、本文を抽出する"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # BeautifulSoupでHTMLを解析
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 本文のテキストを抽出
        # 不要なタグを削除
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # テキストを取得
        text = soup.get_text()
        
        # 余分な空白を削除
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    except requests.RequestException as e:
        print(f"エラー: URLのコンテンツを取得できませんでした: {e}", file=sys.stderr)
        sys.exit(1)

def summarize(text):
    """テキストをシンプルに要約する"""
    try:
        # テキストを分割して最初の数文を取得
        sentences = text.split('.')[:3]  # 最初の3文を取得
        summary = '.'.join(sentences).strip()
        return summary
    except Exception as e:
        print(f"エラー: 要約の生成に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    # コマンドライン引数からURLを取得
    if len(sys.argv) != 2:
        print("使用方法: python summarize.py <URL>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    
    # URLのコンテンツを取得
    content = fetch_content(url)
    
    # コンテンツを要約
    summary = summarize(content)
    
    # 要約を表示
    print(summary)

if __name__ == "__main__":
    main()
