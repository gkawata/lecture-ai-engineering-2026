# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：[search_materials]
- STEP 2 の [tool call]：[glossary_search_glossary]
- STEP 3 の [tool call]：[glossary_search_glossary], [fetch_fetch]
- STEP 4 の [tool call]：
glossary_search_glossary

fetch_fetch

aws_aws___read_documentation

aws_aws___search_documentation

aws_aws___list_regions

aws_aws___get_regional_availability

aws_aws___retrieve_skill

- 気づき・疑問：3種類のMCPサバーについて学んだ。

現在エージェントに接続されている3つのMCPサーバー（計7つのツール）の概要は以下の通りです。

### 3つのMCPサーバーの比較

| サーバー名 | 起動・接続コマンド / URL | サーバーの種類と通信方式 | 提供されるツール（計7個） |
| :--- | :--- | :--- | :--- |
| **`glossary`** | `uv run python -m app.mcp_server` | **ローカルのカスタムサーバー（stdio）**<br>自身のプロジェクト環境内でローカルのPythonコードを直接起動するタイプです。 | 1. `glossary_search_glossary` |
| **`fetch`** | `uvx mcp-server-fetch==2026.11.11 --no-readability-js` | **外部パッケージのローカル実行（stdio）**<br>PyPI上の公式パッケージを `uvx` で一時環境にダウンロード・実行するタイプです。 | 2. `fetch_fetch` |
| **`aws`** | `https://knowledge-mcp.global.api.aws` | **リモートホスト型サーバー（HTTPS / Streamable HTTP）**<br>AWS側でホスティングされているクラウド上のサーバーにHTTPS経由で直接接続するタイプです。 | 3. `aws_aws___read_documentation`<br>4. `aws_aws___search_documentation`<br>5. `aws_aws___list_regions`<br>6. `aws_aws___get_regional_availability`<br>7. `aws_aws___retrieve_skill` |

---

### 各サーバーの特徴

* **`glossary`（自作・ローカル型）**
  * プロジェクトの仮想環境（`uv run`）を使って子プロセスとして起動し、講座（AIE2026）固有の用語集を検索するツールを提供します。
* **`fetch`（既製品・一時実行型）**
  * プロジェクトの依存関係を汚さないよう `uvx` を使って隔離されたキャッシュ環境から起動し、指定されたURLのWebページを取得してMarkdownに変換するツールを提供します。
* **`aws`（クラウド・リモート接続型）**
  * ローカルでプロセスを立ち上げず、AWSが公開しているエンドポイントへネットワーク経由で接続し、AWSドキュメントの検索・閲覧やリージョン情報の取得など5つのツールを提供します。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
