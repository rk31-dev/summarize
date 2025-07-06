#!/bin/bash

# 環境変数を読み込む
source .env

# Pythonスクリプトを実行
python3 summarize.py "$@"
