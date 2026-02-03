@echo off
REM 翻訳エディタ起動スクリプト (Windows)

cd /d "%~dp0"

echo =========================================
echo   翻訳エディタを起動しています...
echo =========================================
echo.

REM Pythonのバージョンチェック
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo エラー: Pythonが見つかりません
    echo Python 3.7以上をインストールしてください
    pause
    exit /b 1
)

python --version
echo.
echo サーバーを起動中...
echo ブラウザで以下のURLを開いてください:
echo   http://localhost:8000/translation_editor.html
echo.
echo 終了するには Ctrl+C を押してください
echo =========================================
echo.

REM ブラウザを自動的に開く（5秒後）
start /b timeout /t 5 /nobreak >nul 2>&1 && start http://localhost:8000/translation_editor.html

REM サーバーを起動
python server.py

pause
