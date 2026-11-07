# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：glossary.jsonを道具として呼ぶ
- `--trace` で見えたツール呼び出し（ツール名と引数）：
モデルに見えているツール: 3 個

[search_glossary]
  講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。
  
  AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について
  答える前に使うこと。query には調べたい用語を1つだけ入れる（例: "LoRA"）。
  引数: {"query": {"type": "string"}}

[get_lecture_summary]
  指定した回（1始まりの整数）の講義の要点を返す。
  
  「第3回では何を学ぶ？」のように、回の内容や関係を聞かれたときに使う。
  引数: {"lecture": {"type": "integer"}}

[make_quiz]
  指定した回の用語から1つを選び、確認問題と答えを返す。
  
  「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。
  引数: {"lecture": {"type": "integer"}}

- 1つの質問での LLM 呼び出し回数（`requests`）：2
- 追加したツールと、docstring に書いた説明：

def make_quiz(lecture: int) -> str:
    """指定した回の用語から1つを選び、確認問題と答えを返す。

    「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。
    """
    terms = [entry for entry in load_glossary() if entry["lecture"] == lecture]
    if not terms:
        return f"第{lecture}回の用語は用語集にありません。"

    entry = random.choice(terms)
    return json.dumps(
        {
            "lecture": lecture,
            "question": f"次の説明に当てはまる用語は何ですか？ {entry['definition']}",
            "answer": entry["term"],
        },
        ensure_ascii=False,
    )


## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展 → 発展
- やったこと：pydantic_aiをgoogle.adk libraryに書き換えた。そして、次の筆問を聞いた。
PYTHONPATH=. uv run --with google-adk python -m adk_agent.glossary_agent.agent --trace "LoRAとは何 ですか？"
[user]: LoRA とQLoRAの違いは？
[glossary_agent]: LoRAとQLoRAの違いは以下の通りです。

* **LoRA（Low-Rank Adaptation）**
  事前学習済みの重みを固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法です。学習するパラメータが少なく、学習結果も小さなファイルで保存できます。

* **QLoRA（Quantized LoRA）**
  ベースモデルの重みを4ビットなどに量子化してメモリを大きく節約したうえで、LoRAによる学習を行う手法です。これにより、より大きなモデルを小さなGPU環境でも扱えるようになります。


PYTHONPATH=. uv run --with google-adk python -m adk_agent.glossary_agent.agent --trace "LoRAとは何 ですか？"
<frozen runpy>:128: RuntimeWarning: 'adk_agent.glossary_agent.agent' found in sys.modules after import of package 'adk_agent.glossary_agent', but prior to execution of 'adk_agent.glossary_agent.agent'; this may result in unpredictable behaviour
[model] gemini-3.5-flash-lite
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
**LoRA（Low-Rank Adaptation）**とは、事前学習済みのモデルの重みを固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを効率的に学習するPEFT（Parameter-Efficient Fine-Tuning）手法のことです。

学習するパラメータ数を大幅に減らすことができ、学習結果（アダプタ）を小さなファイルサイズで保存できるというメリットがあります。本講座の演習でも実際に扱います。

関連する回：第2回

--- trace ---
[tool call]   search_glossary({"query": "LoRA"})
[tool return] search_glossary -> {'result': '[{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するP…
[usage] cache_tokens_details=None cached_content_token_count=None candidates_token_count=116 candidates_tokens_details=None prompt_token_count=763 prompt_tokens_details=[ModalityTokenCount(
  modality=<MediaModality.TEXT: 'TEXT'>,
  token_count=763
)] thoughts_token_count=None tool_use_prompt_token_count=None tool_use_prompt_tokens_details=None total_token_count=879traffic_type=None


$ PYTHONPATH=. uv run --with google-adk python -m adk_agent.glossary_agent.agent --trace "第3回の確認問題を出して"
<frozen runpy>:128: RuntimeWarning: 'adk_agent.glossary_agent.agent' found in sys.modules after import of package 'adk_agent.glossary_agent', but prior to execution of 'adk_agent.glossary_agent.agent'; this may result in unpredictable behaviour
[model] gemini-3.5-flash-lite
Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY.
第3回の内容から確認問題をお出しします！

**【確認問題】**
次の説明に当てはまる用語は何ですか？
「LLMが自分で判断してツールを呼び出し、その結果を見てさらに次の行動を決める、というループで目的を達成するシステム。基本構造は『モデル＋ループ＋ツール』。」

ぜひ考えてみてくださいね。

（関連する回：第3回）

--- trace ---
[tool call]   make_quiz({"lecture": 3})
[tool return] make_quiz -> {'result': '{"lecture": 3, "question": "次の説明に当てはまる用語は何ですか？ LLMが自分で判断してツールを呼び出し、その結果を見てさらに次の行動を決める、というループで目的を達成するシステム。基本構…
[usage] cache_tokens_details=None cached_content_token_count=None candidates_token_count=88 candidates_tokens_details=None prompt_token_count=551 prompt_tokens_details=[ModalityTokenCount(
  modality=<MediaModality.TEXT: 'TEXT'>,
  token_count=551
)] thoughts_token_count=None tool_use_prompt_token_count=None tool_use_prompt_tokens_details=None total_token_count=639 traffic_type=None

- 結果：google adkを使っても問題なくToolの呼び出しをして結果がでる。
- 気づき・疑問：大きな違いは、エージェントの実行をどこが担うかです。Pydantic AIでは、Agentに指示やツールを登録し、run_sync()などを呼び出して実行します。結果も呼び出し元に直接返るため、通常のPython関数に近い感覚で扱えます。一方、Google ADKでは、Agentは主に設定を表し、実行はRunnerが担います。会話はセッションとして管理され、実行中のやりとりはイベントとして流れます。また、adk runやadk webなど、エージェントを試すための専用CLI・開発環境が用意されています。つまり、Pydantic AIはPythonコードから直接呼び出す簡潔さ、Google ADKはセッション管理や専用ランタイムを含むエージェント開発基盤としての一体感が特徴です。どちらもツール呼び出しやモデル連携ができますが、実行・状態管理の設計が異なります。
