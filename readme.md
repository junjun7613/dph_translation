# 翻訳エディタ

LLM翻訳の手動修正を支援するWebベースの翻訳エディタです。

## 機能

- **3列表示**: 英語原文 | LLM翻訳（参考） | 日本語訳（編集可）
- **差分ハイライト**: LLM翻訳と手動修正版の差分を自動表示
- **コメント機能**: 翻訳箇所にコメントを付けて共有
- **自動保存**: 編集内容を自動的にタイムスタンプ付きで保存

## セットアップ

### 必要な環境

- Python 3.7以上
- モダンなWebブラウザ（Chrome、Firefox、Safari、Edge）

### インストール手順

1. **ファイルの配置**
   - このフォルダを任意の場所に配置してください

2. **データの準備**
   - `data/` フォルダ内に翻訳プロジェクトのフォルダを作成
   - 例: `data/introduction/`
   - 必要に応じて `original/` サブフォルダにLLM翻訳原文を配置

### 使い方

#### macOS / Linux の場合

1. ターミナルで以下を実行:
   ```bash
   ./start.sh
   ```

2. ブラウザで自動的に開かれます
   - または手動で `http://localhost:8000/translation_editor.html` を開く

#### Windows の場合

1. `start.bat` をダブルクリック

2. ブラウザで `http://localhost:8000/translation_editor.html` を開く

#### 手動起動の場合

```bash
python3 server.py
```

ブラウザで `http://localhost:8000/translation_editor.html` を開いてください。

### 終了方法

ターミナル/コマンドプロンプトで `Ctrl + C` を押してください。

## ディレクトリ構造

```
translation-editor/
├── README.md                    # このファイル
├── server.py                    # サーバープログラム
├── translation_editor.html      # エディタ画面
├── start.sh                     # 起動スクリプト（macOS/Linux）
├── start.bat                    # 起動スクリプト（Windows）
└── data/                        # データフォルダ
    └── {project_name}/          # プロジェクトごとのフォルダ
        ├── original/            # LLM翻訳原文（参考用）
        │   └── *.csv
        ├── comments/            # コメントデータ（自動生成）
        │   └── *.json
        └── *_edited_*.csv       # 編集済みファイル（自動生成）
```

## CSVファイルフォーマット

CSVファイルは以下の4列で構成されます:

```csv
id,kind,text_en,text_ja
1,title,"Original English Text","日本語訳"
2,body,"Another paragraph","別の段落"
```

- `id`: エントリID
- `kind`: テキストタイプ（title, abstract, keyword, body）
- `text_en`: 英語原文
- `text_ja`: 日本語訳

## コメント機能

### コメントの追加

1. 日本語訳のテキストを選択
2. 「💬 コメント追加」ボタンをクリック
3. 作成者を選択（小川、後藤、原）
4. コメントを入力して保存

### コメントの表示・編集

- 💬アイコンにマウスを重ねるとコメント内容が表示されます
- 💬アイコンをクリックすると編集ダイアログが開きます

## ファイル保存

「修正済みCSVを保存」ボタンをクリックすると、以下の形式で保存されます:

- 初回保存: `{filename}_edited_YYYYMMDD_HHMMSS.csv`
- 2回目以降: 日時部分のみ更新

例:
```
introduction.csv
  ↓ 編集して保存
introduction_edited_20260203_143000.csv
  ↓ さらに編集して保存
introduction_edited_20260203_150000.csv
```

## トラブルシューティング

### ポートが使用中のエラー

```
OSError: [Errno 48] Address already in use
```

**解決方法**:
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID [PID番号] /F
```

### ファイルが表示されない

1. `data/` フォルダの構造を確認
2. CSVファイルが正しい形式か確認
3. サーバーを再起動

### ブラウザでページが開けない

1. サーバーが起動しているか確認
2. `http://localhost:8000/translation_editor.html` のURLが正しいか確認
3. 別のブラウザで試してみる

## バージョン履歴

- v1.0.0 (2026-02-03): 初版リリース
  - 3列表示
  - 差分ハイライト
  - コメント機能
  - 作成者選択機能

## サポート

問題や質問がある場合は、プロジェクト管理者にお問い合わせください。

## ライセンス

このソフトウェアは翻訳プロジェクトチーム内での使用に限定されます。
