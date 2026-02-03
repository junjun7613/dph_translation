#!/bin/bash
# 翻訳エディタ起動スクリプト (macOS/Linux)

cd "$(dirname "$0")"

echo "========================================="
echo "  翻訳エディタを起動しています..."
echo "========================================="
echo ""

# Pythonのバージョンチェック
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "エラー: Pythonが見つかりません"
    echo "Python 3.7以上をインストールしてください"
    exit 1
fi

echo "Python: $($PYTHON_CMD --version)"
echo ""
echo "サーバーを起動中..."
echo "ブラウザで以下のURLを開いてください:"
echo "  http://localhost:8000/translation_editor.html"
echo ""
echo "終了するには Ctrl+C を押してください"
echo "========================================="
echo ""

# ブラウザを自動的に開く（5秒後）
(sleep 5 && open http://localhost:8000/translation_editor.html 2>/dev/null) &

# サーバーを起動
$PYTHON_CMD server.py
