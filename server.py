#!/usr/bin/env python3
"""
翻訳エディタ用の簡易HTTPサーバー
dataフォルダ内のCSVファイル一覧を取得し、選択したCSVを読み込めるようにします
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from datetime import datetime

class TranslationEditorHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        # CORSヘッダーを追加
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)

        # フォルダ一覧を取得するAPI
        if parsed_path.path == '/api/folders':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            data_dir = Path('data')
            folders = []

            if data_dir.exists():
                # dataフォルダ直下のサブフォルダを取得
                for item in data_dir.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        folders.append(item.name)
                folders.sort()

            response = {'folders': folders}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return

        # 特定フォルダ内のCSVファイル一覧を取得するAPI
        elif parsed_path.path.startswith('/api/csv-files/'):
            folder_name = parsed_path.path.replace('/api/csv-files/', '')
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            folder_path = Path('data') / folder_name
            csv_files = []

            if folder_path.exists() and folder_path.is_dir():
                # 指定フォルダ内のCSVファイルを取得
                for csv_file in folder_path.glob('*.csv'):
                    csv_files.append({
                        'name': csv_file.name,
                        'display_name': csv_file.name,
                        'is_original': False
                    })

                # originalフォルダ内のCSVファイルも取得
                original_path = folder_path / 'original'
                if original_path.exists() and original_path.is_dir():
                    for csv_file in original_path.glob('*.csv'):
                        # メインフォルダに同名ファイルがあるかチェック
                        if not any(f['name'] == csv_file.name for f in csv_files):
                            csv_files.append({
                                'name': csv_file.name,
                                'display_name': f'{csv_file.name} (LLM原文)',
                                'is_original': True
                            })

                # ファイル名でソート
                csv_files.sort(key=lambda x: x['name'])

            response = {'files': csv_files}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            return

        # 指定されたCSVファイルの内容を取得するAPI（編集用とLLM原文の両方）
        elif parsed_path.path.startswith('/api/csv-content/'):
            relative_path = parsed_path.path.replace('/api/csv-content/', '')
            file_path = Path('data') / relative_path

            if file_path.exists() and file_path.suffix == '.csv':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                # 編集用のCSVを読み込む
                with open(file_path, 'r', encoding='utf-8') as f:
                    csv_content = f.read()

                # originalフォルダ内の同名ファイルを探す
                original_content = None
                parts = relative_path.split('/')

                # original/xxx.csvの形式で指定された場合
                if len(parts) >= 3 and parts[1] == 'original':
                    folder_name = parts[0]
                    file_name = parts[2]
                    # この場合、csv_contentが既にoriginalの内容なので、それをoriginal_contentにも設定
                    original_content = csv_content
                    # csv_contentはNoneにして、クライアント側でoriginalを使うようにする
                    csv_content = None
                elif len(parts) >= 2:
                    folder_name = parts[0]
                    file_name = parts[1]

                    # editedファイルの場合、元のファイル名を取得
                    import re
                    edited_pattern = r'^(.+)_edited_\d{8}_\d{6}\.csv$'
                    match = re.match(edited_pattern, file_name)
                    if match:
                        original_file_name = match.group(1) + '.csv'
                    else:
                        original_file_name = file_name

                    original_path = Path('data') / folder_name / 'original' / original_file_name

                    if original_path.exists():
                        with open(original_path, 'r', encoding='utf-8') as f:
                            original_content = f.read()

                response = {
                    'csv_content': csv_content,
                    'original_content': original_content
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'File not found'}).encode('utf-8'))
                return

        # コメントデータを取得するAPI
        elif parsed_path.path.startswith('/api/comments/'):
            relative_path = parsed_path.path.replace('/api/comments/', '')
            # relative_pathの形式: folder_name/file_name.csv
            parts = relative_path.split('/')
            if len(parts) >= 2:
                folder_name = parts[0]
                file_name = parts[1].replace('.csv', '')

                # commentsフォルダ内のJSONファイルを探す
                comments_path = Path('data') / folder_name / 'comments' / f'{file_name}.json'

                if comments_path.exists():
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()

                    with open(comments_path, 'r', encoding='utf-8') as f:
                        comments_data = f.read()

                    self.wfile.write(comments_data.encode('utf-8'))
                    return
                else:
                    # コメントファイルが存在しない場合は空のオブジェクトを返す
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({}).encode('utf-8'))
                    return
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid path'}).encode('utf-8'))
                return

        # その他のリクエストは通常のファイルサーバーとして処理
        super().do_GET()

    def do_POST(self):
        parsed_path = urlparse(self.path)

        # CSV保存API
        if parsed_path.path == '/api/save-csv':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            original_path = data.get('originalPath')
            csv_content = data.get('csvContent')

            if not original_path or not csv_content:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid request'}).encode('utf-8'))
                return

            # 元のファイルパス
            original_file = Path('data') / original_path

            # originalフォルダから読み込んだ場合は、親フォルダに保存
            if 'original' in original_file.parts:
                # original/xxx.csvの形式の場合、親フォルダに保存
                parts = original_path.split('/')
                if len(parts) >= 3 and parts[1] == 'original':
                    folder_name = parts[0]
                    file_name = parts[2]
                    file_dir = Path('data') / folder_name
                    file_stem = Path(file_name).stem
                else:
                    file_stem = original_file.stem
                    file_dir = original_file.parent
            else:
                # ファイル名と拡張子を分離
                file_stem = original_file.stem
                file_dir = original_file.parent

            # 現在の日時を取得（YYYYMMDD_HHMMSS形式）
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

            # ファイル名が既に _edited_YYYYMMDD_HHMMSS の形式か確認
            import re
            edited_pattern = r'^(.+)_edited_\d{8}_\d{6}$'
            match = re.match(edited_pattern, file_stem)

            if match:
                # 既に編集済みファイルの場合、元の名前を維持して日時のみ更新
                base_name = match.group(1)
                new_filename = f"{base_name}_edited_{timestamp}.csv"
            else:
                # 初めての編集の場合
                new_filename = f"{file_stem}_edited_{timestamp}.csv"

            new_file_path = file_dir / new_filename

            try:
                # ディレクトリが存在しない場合は作成
                file_dir.mkdir(parents=True, exist_ok=True)

                # CSVファイルを保存
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    f.write(csv_content)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                response = {
                    'success': True,
                    'filename': new_filename,
                    'path': str(new_file_path.relative_to(Path('data')))
                }
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                return

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                return

        # コメント保存API
        elif parsed_path.path == '/api/save-comments':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            file_path = data.get('filePath')  # folder_name/file_name.csv
            comments_data = data.get('commentsData')  # コメントオブジェクト

            if not file_path or comments_data is None:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid request'}).encode('utf-8'))
                return

            # ファイルパスを解析
            parts = file_path.split('/')
            if len(parts) >= 2:
                folder_name = parts[0]
                # originalパスの場合は除去
                if len(parts) == 3 and parts[1] == 'original':
                    file_name = parts[2].replace('.csv', '')
                else:
                    file_name = parts[1].replace('.csv', '')

                # commentsフォルダを作成
                comments_dir = Path('data') / folder_name / 'comments'
                comments_dir.mkdir(parents=True, exist_ok=True)

                # JSONファイルに保存
                comments_file = comments_dir / f'{file_name}.json'

                try:
                    with open(comments_file, 'w', encoding='utf-8') as f:
                        json.dump(comments_data, f, ensure_ascii=False, indent=2)

                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()

                    response = {
                        'success': True,
                        'path': str(comments_file.relative_to(Path('data')))
                    }
                    self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                    return

                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                    return
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid file path'}).encode('utf-8'))
                return

        # その他のPOSTリクエストは404
        self.send_response(404)
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TranslationEditorHandler)
    print(f'翻訳エディタサーバーを起動しました')
    print(f'ブラウザで以下のURLを開いてください:')
    print(f'  http://localhost:{port}/translation_editor.html')
    print(f'\nサーバーを停止するには Ctrl+C を押してください')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
