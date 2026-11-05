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

- 取り組んだレベル：基礎 / 実装 / 発展
- やったこと：
- 結果：
- 気づき・疑問：
