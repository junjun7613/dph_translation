# 翻訳エディタ配布ガイド

このドキュメントは、翻訳エディタをチームメンバーに配布する際の手順を説明します。

## 配布方法の選択

### オプション1: Gitリポジトリ（推奨）

**メリット**:
- 更新配布が簡単
- バージョン管理が容易
- データは各自のローカルに保持

**手順**:

1. **Gitリポジトリの準備**
   ```bash
   cd /path/to/dph_translation
   git init
   git add .
   git commit -m "Initial commit: Translation Editor v1.0.0"
   ```

2. **リモートリポジトリにプッシュ**（GitHub/GitLab/Bitbucket等）
   ```bash
   git remote add origin <リポジトリURL>
   git push -u origin main
   ```

3. **チームメンバーへの共有**
   - リポジトリURLをチームに共有
   - 各メンバーは以下を実行:
   ```bash
   git clone <リポジトリURL>
   cd dph_translation
   ./start.sh  # macOS/Linux
   # または start.bat をダブルクリック (Windows)
   ```

4. **更新配布**
   ```bash
   # 管理者側
   git add .
   git commit -m "Update: 新機能追加"
   git push

   # メンバー側
   git pull
   ```

### オプション2: ZIPファイル配布

**メリット**:
- Git不要
- シンプル

**手順**:

1. **配布用ZIPを作成**
   ```bash
   # 以下のファイル/フォルダを含める:
   # - README.md
   # - server.py
   # - translation_editor.html
   # - start.sh
   # - start.bat
   # - data/.gitkeep (空のdataフォルダ用)

   zip -r translation-editor-v1.0.0.zip \
     README.md \
     server.py \
     translation_editor.html \
     start.sh \
     start.bat \
     data
   ```

2. **配布**
   - メールやファイル共有サービスでZIPを配布
   - チームメンバーは解凍後、start.shまたはstart.batを実行

3. **更新配布**
   - 新しいバージョンのZIPを作成して配布
   - メンバーは古いファイルを上書き（dataフォルダは保持）

### オプション3: Docker配布（技術的なチーム向け）

**メリット**:
- 環境依存なし
- セットアップ不要

**手順**:

1. **Dockerfileを作成**（プロジェクトルートに配置）
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY server.py translation_editor.html ./
   EXPOSE 8000
   CMD ["python", "server.py"]
   ```

2. **docker-compose.ymlを作成**
   ```yaml
   version: '3.8'
   services:
     translation-editor:
       build: .
       ports:
         - "8000:8000"
       volumes:
         - ./data:/app/data
   ```

3. **配布**
   - Dockerfile、docker-compose.yml、README.mdを配布
   - メンバーは以下を実行:
   ```bash
   docker-compose up
   ```

## データ共有の方法

各メンバーのローカル環境で独立して作業する場合と、データを共有する場合で異なります。

### ケース1: 完全独立作業

- 各メンバーが自分の `data/` フォルダを管理
- `.gitignore` でデータフォルダを除外済み
- 編集結果は別途共有（メール、共有ドライブ等）

### ケース2: 共有ドライブ利用

**手順**:
1. Google Drive、Dropbox等に共有 `data/` フォルダを作成
2. 各メンバーはローカルに同期
3. シンボリックリンクを作成:
   ```bash
   # macOS/Linux
   ln -s ~/Dropbox/translation-project/data ./data

   # Windows (管理者権限で実行)
   mklink /D data "C:\Users\YourName\Dropbox\translation-project\data"
   ```

**注意**:
- 同時編集は避ける
- ファイル名に日時が入るため、各自の編集を追跡可能

### ケース3: Gitでデータも管理

**手順**:
1. `.gitignore` から `data/` を削除
2. データをコミット:
   ```bash
   git add data/
   git commit -m "Add translation data"
   git push
   ```

**注意**:
- ファイルサイズが大きい場合、Git LFSの利用を検討
- マージコンフリクトに注意

## チーム向け配布チェックリスト

- [ ] README.mdを最新に更新
- [ ] コメント作成者リストを確認（translation_editor.html:260）
- [ ] サンプルデータの用意（オプション）
- [ ] テスト実行（各OS環境）
- [ ] 配布方法の選択と準備
- [ ] チームへの使い方説明資料の準備
- [ ] サポート体制の確立

## トラブルシューティング資料

チームメンバー向けに以下の情報を共有することを推奨します:

### よくある質問

**Q: Pythonがインストールされているか確認するには？**
```bash
python3 --version
# または
python --version
```

**Q: 別のポート番号を使いたい**
A: server.py の最終行を変更:
```python
run_server(port=8080)  # 8000から8080に変更
```

**Q: 複数人で同じファイルを編集したい**
A: タイムスタンプ付きファイル名で保存されるため、各自の編集を後でマージ可能

## バージョン管理

バージョン番号の付け方:
- v1.0.0: 初版
- v1.1.0: 新機能追加
- v1.0.1: バグ修正

配布時は必ずバージョン番号をREADME.mdとファイル名に含める。

## セキュリティ注意事項

- **ローカルネットワーク外からのアクセス不可**: 現在の設定では localhost のみ
- **パスワード保護なし**: ローカル環境での使用を想定
- **データの機密性**: `data/` フォルダは適切に管理すること
- **公開リポジトリに注意**: 機密データが含まれる場合はプライベートリポジトリを使用

## サポート連絡先

技術的な問題や質問がある場合の連絡先:
- Email: [管理者のメールアドレス]
- チャット: [SlackチャンネルやTeamsチャネル]
- Issue Tracker: [GitHubのIssuesページ等]

## ライセンスと利用規約

このソフトウェアは [プロジェクト名] 翻訳プロジェクト内での使用に限定されます。
外部への配布や商用利用は禁止します。
