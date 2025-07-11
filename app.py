from flask import Flask, request, render_template_string
import os
from summarize import fetch_content, summarize

app = Flask(__name__)

# HTMLテンプレート
TEMPLATE = '''
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ウェブページ要約ツール</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .input-group {
            margin-bottom: 20px;
        }
        input[type="url"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>ウェブページ要約ツール</h1>
        <div class="input-group">
            <input type="url" id="url" placeholder="URLを入力してください">
            <button onclick="summarize()">要約を生成</button>
        </div>
        <div id="result" class="result"></div>
    </div>

    <script>
        async function summarize() {
            const url = document.getElementById('url').value;
            if (!url) {
                alert('URLを入力してください');
                return;
            }

            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '要約を生成中...';

            try {
                const response = await fetch('/summarize', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: url })
                });
                
                const data = await response.json();
                resultDiv.innerHTML = `<p>${data.summary}</p>`;
            } catch (error) {
                resultDiv.innerHTML = `<p style="color: red;">エラーが発生しました: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(TEMPLATE)

@app.route('/summarize', methods=['POST'])
def summarize_endpoint():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return {'error': 'URLが指定されていません'}, 400
    
    try:
        content = fetch_content(url)
        summary = summarize(content)
        return {'summary': summary}
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/build')
def build():
    # ビルドコマンドの実行
    return 'Build successful'

if __name__ == '__main__':
    app.run(debug=True)
