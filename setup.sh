#!/bin/bash

# APIキーを環境変数に設定
export GOOGLE_API_KEY="AIzaSyAnl4hKgwG_460LUpW1SAVx0NEKy7AiOI4"

# Pythonスクリプトを実行
python3 summarize.py "$@"
