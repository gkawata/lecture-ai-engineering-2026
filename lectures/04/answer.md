# 第4回 解答

## 演習

- 基準別の一致率（直す前）：根拠　/　、範囲　/　、ヒント　/　、分かりやすさ　/　、回の表示　/　下記の通り
基準別の一致率（自分のラベルと LLM の判定、10 件）
  根拠                7/9    要確認 1
  範囲                9/10
  ヒント             10/10
  分かりやすさ        9/10
  回の表示（コード）  7/10
総合の一致率   6/9   （自動判定できた 9/10 件 = coverage 90%）


- 要確認の件数（直す前）：1件

[model] gemini-3.5-flash-lite  temperature=0  rubric=data/eval/rubric.md
採点中 10 件 ..........

基準別の一致率（自分のラベルと LLM の判定、10 件）
  根拠                7/9    要確認 1
  範囲                9/10
  ヒント             10/10
  分かりやすさ        9/10
  回の表示（コード）  7/10
総合の一致率   6/9   （自動判定できた 9/10 件 = coverage 90%）

要確認 1 件（LLM が unsure にした項目。人が見る）
  #05 根拠: 用語集にないこと適切に伝えたうえで一般的な説明をしているが、これは最後の「まだ決めていないこと」に該当するため。

不一致 7 件
  #02 回の表示     過検出（LLM=fail 自分=pass）  理由: 末尾（最後の行）に「第N回」があるかをコードで判定
  #04 分かりやすさ 過検出（LLM=fail 自分=pass）  理由: 同じ内容の言い換えや繰り返しが複数含まれているため、簡潔さという点で課題があります。
  #06 根拠         過検出（LLM=fail 自分=pass）  理由: 用語集の内容や宿題の要件を踏まえているが、参照の期待するふるまいと直接矛盾している。
  #07 回の表示     過検出（LLM=fail 自分=pass）  理由: 末尾（最後の行）に「第N回」があるかをコードで判定
  #09 回の表示     過検出（LLM=fail 自分=pass）  理由: 末尾（最後の行）に「第N回」があるかをコードで判定
  #10 根拠         過検出（LLM=fail 自分=pass）  理由: 「追加される予定なので」と断定しており、参照の「用語集・要点データにないこと（追加の予定など）は断定しない」という期待するふるまいに違反している。
  #10 範囲         見逃し（LLM=pass 自分=fail）  理由: 講座の第14回についての質問に対して適切に応答しており、講座の範囲内で答えられている。

→ lectures/04/judge_result.json に保存しました





- 直した基準と、書き足した方針：根拠に次を足したー＞- 用語集にない語を、「用語集にはない」と伝えたうえで
一般的に説明するのは、断定ではない（pass）

削除したものー＞## まだ決めていないこと（当てはまる回答は unsure にする）
- 用語集にない語について、「用語集にはない」と伝えたうえで
一般的な説明をすることが、「推測で断定する」にあたるかどうか

- 基準別の一致率と要確認の件数（直した後）：

[model] gemini-3.5-flash-lite  temperature=0  rubric=data/eval/rubric.md
採点中 10 件 ..........

基準別の一致率（自分のラベルと LLM の判定、10 件）
  根拠                8/10
  範囲                8/10
  ヒント             10/10
  分かりやすさ        9/10
  回の表示（コード）  7/10
総合の一致率   7/10   （自動判定できた 10/10 件 = coverage 100%）

要確認 0 件（LLM が unsure にした項目。人が見る）

不一致 8 件
  #02 回の表示     過検出（LLM=fail 自分=pass）  理由: 末尾（最後の行）に「第N回」があるかをコードで判定
  #04 分かりやすさ 過検出（LLM=fail 自分=pass）  理由: 同じ内容の言い換えや繰り返しが複数含まれており、簡潔ではないため不合格とします。
  #06 範囲         見逃し（LLM=pass 自分=fail）  理由: 講座の範囲内である第3回の宿題に関する質問に答えており、範囲外ではないため。
  #07 回の表示     過検出（LLM=fail 自分=pass）  理由: 末尾（最後の行）に「第N回」があるかをコードで判定
  #08 根拠         過検出（LLM=fail 自分=pass）  理由: 用語集にない事柄について推測や断定ではなく全文を出力してしまっており、期待するふるまいに反している。
  #09 回の表示     過検出（LLM=fail 自分=pass）  理由: 末尾（最後の行）に「第N回」があるかをコードで判定
  #10 根拠         過検出（LLM=fail 自分=pass）  理由: 「追加される予定なので」と用語集にない推測の断定を行っているため、期待するふるまいに違反しています。
  #10 範囲         見逃し（LLM=pass 自分=fail）  理由: 講座の範囲である第14回の要点について適切に応答しています。


- 講師のラベルと自分のラベルで判定が違った項目と、そう判定した理由：

### Summary of Metrics between first run vs second run

| Metric / Criterion | Output 1 (Baseline) | Output 2 (`gemini-3.5-flash-lite`) | Change |
| :--- | :--- | :--- | :--- |
| **Header Metadata** | *None* | `[model] gemini-3.5-flash-lite temperature=0 rubric=data/eval/rubric.md` | Added run configuration details |
| **Overall Agreement** | **6/9** (66.7%) | **7/10** (70.0%) | **+1** overall match |
| **Coverage** | **90%** (9/10 auto-graded) | **100%** (10/10 auto-graded) | **+10%** (0 items left for human review) |
| **Needs Review (`要確認`)** | **1** (`#05 根拠`) | **0** | Resolved `#05` |
| **Total Mismatches (`不一致`)** | **7** | **8** | **+1** mismatch (due to `#05` entering the pool and shifts in `#06`/`#08`) |
| **根拠 (Grounding)** | 7/9 (1 unsure) | 8/10 | `#05` & `#06` now match; `#08` became a mismatch |
| **範囲 (Scope)** | 9/10 | 8/10 | `#06` became a new mismatch |
| **ヒント (Hints)** | 10/10 | 10/10 | No change |
| **分かりやすさ (Clarity)** | 9/10 | 9/10 | No change (same `#04` mismatch) |
| **回の表示 (Code check)** | 7/10 | 7/10 | No change (same `#02`, `#07`, `#09` mismatches) |


- 気づき・疑問：

### 1. LLM-as-a-Judge フレームワークにおける示唆

* **LLM は「言外の意図」を汲み取らず、文字通りのルールに従う**
  * LLM 評価器は人間の「常識的な許容範囲」を自動では補完してくれません。
  * 人間が「これもOKだろう」と思っているエッジケース（例：全文出力など）は、ルーブリックに明記しない限り「定義外 ＝ 不合格」とみなされる傾向があります。

* **ルーブリックの設計は「ソフトウェア開発のテスト駆動」と同じ**
  * 1つのケース（`#05`）を通すためにルールを修正すると、別のケース（`#08`）が壊れる（リグレッションが起きる）ことがあります。
  * 評価基準は一度作って終わりではなく、不一致ログを見ながら継続的にリファクタリングしていくプロセスが不可欠です。

* **`unsure`（保留）の設計は初期フェーズで非常に有効**
  * いきなり 100% の自動判定を目指すのではなく、1回目のように `unsure` を設けて「LLM が迷う境界線」を炙り出します。
  * その境界線を人間が確認してルールに落とし込むサイクル（**Human-in-the-Loop**）が、最も効率的に精度を高めます。

---

### 2. 人間の評価者（アノテーター）に求められること

* **評価者自身が評価基準（ルーブリック）を深く、一貫して理解している必要がある**
  * LLM-as-a-Judge の精度は、正解データ（自分のラベル）の品質に完全に依存します。
  * 人間側が「なんとなくこれは pass」「これは雰囲気的に fail」と感覚でラベルを付けていると、LLM の判定とズレたときに「LLM が間違っているのか、自分の基準がブレているのか」が判別できなくなります。

* **「なぜ自分がそのラベルを付けたのか」を言語化できる状態にする**
  * 今回 `#05` のルールを明確に言語化できたからこそ、LLM の判定を改善できました。
  * 人間の評価者が各基準（`根拠` と `範囲` の違いなど）の定義と境界線を腹落ちさせたうえでラベリングを行うことが、結果として LLM への最も的確な指示（プロンプト設計）につながります。


## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展 -> 発展
- やったこと：Open AIが開発した新しいベンチマークLifeValについて学んだ。https://arxiv.org/html/2611.06687v1

- 結果：英語で記載します。

# LifeVal: Benchmark Summary

**Source:** *LifeVal: Evaluating AI Model Performance on Personalized Agentic Consumer Tasks* (`arXiv:2611.06687v1`, November 4, 2026)  
**Authors:** Jenny Yang, Elizabeth Proehl, Anjan Bharadwaj, Emily Fan, Charlotte Cole, James Kim, Noam Brown, Phoebe Thacker, Amelia Glaese, Tejal Patwardhan (OpenAI)

**Summary** LifeVal (Evaluating AI Model Performance on Personalized Agentic Consumer Tasks) uses a multi-stage human and automated verification process, relies on several distinct groups of participants, and evaluates frontier OpenAI models across 169 personalized tasks.
---

## 1. Verification & Quality Control Methodology

To ensure tasks are realistic, solvable, and accurately graded despite their subjective nature, the authors implemented a dual-track verification pipeline alongside automated grading checks:

### Three-Round Human Quality Control (QC)
Every task had to pass at least three rounds of human review before inclusion:
1. **Peer Review:** Another task writer with relevant domain expertise assessed practical accuracy, realism, and completeness.
2. **Lead Review:** A trained reviewer verified that the task met difficulty standards and was fair (i.e., solvable using only the provided context).
3. **Final Sign-Off:** A third expert reviewer performed a final inspection and approved the task.

### Parallel Model-Driven QC
- A model attempted each task using the prompt, personal context, and Reinforcement Learning Environment (RLE).
- A second model reviewed the attempt to classify any failures (rubric flaws, missing context, environment bugs, or model errors) and proposed targeted fixes.
- Human reviewers decided whether to apply the proposed fixes.

### Privacy & De-identification
- Task writers replaced Personally Identifiable Information (PII) with synthetic data.
- Writers consented to share their ChatGPT conversation histories and memories, which were de-identified prior to research use.

### Automated & Anti-Hacking Grading
Task completions were scored using two automated graders powered by **GPT-5.6** (specifically GPT-5.6 Sol with `xhigh` reasoning):
- **Primary Grader:** Evaluates each rubric item independently against the model's final response, created files/artifacts, and backend RLE state diffs.
- **Hack Grader:** Monitors whether the model accessed internal RLE APIs to bypass realistic web constraints; any detected environment hacking results in a score of `0`.
- **Human Grader Alignment:** To verify the automated grader, **17 human trainers** independently graded a subset of 30 rollouts, achieving an average score of **83.61%** compared to GPT-5.6's **84.20%** (Pearson correlation $r = 0.864$).

---

## 2. People Involved

While the exact total headcount of task writers is not specified, the paper breaks down the human participants across three main groups:

| Group | Count | Role & Details |
| :--- | :--- | :--- |
| **Researchers & Contributors** | 10 authors + 33 acknowledged | OpenAI research team and internal contributors. |
| **Survey Respondents** | 3,837 initial / **1,826 retained** | Demographically representative U.S. consumers screened via comprehension and attention checks to establish the 148-category value distribution (cross-referenced against ATUS $n=7,700$ and MTUS $n=8,782$). |
| **Expert Task Writers & Reviewers** | Unspecified total (min. **3 reviewers/task** + **17 grader validators**) | Recruited from generalist pools and targeted niche outreach (e.g., ADU setup, mold remediation). Writers had to personally complete the task multiple times and see real-world results through for over a year. |

---

## 3. Benchmark Evaluation & Findings

The authors evaluated **GPT-5.2, GPT-5.4, GPT-5.5, GPT-5.6, and GPT-6 Astra** across **169 finalized tasks** (with an 8-hour timeout per rollout):

- **Progression Across Model Generations:** Performance (measured by mean reward) improved steadily from GPT-5.2 through GPT-6 Astra due to stronger computer-use, browser-use, and connector capabilities. GPT-5.2 was the only model to frequently run out of tokens without producing a final answer.
- **Alignment & Decision-Boundary Trade-offs:** **GPT-6 Astra**, the most aligned model tested, showed higher failure rates in categories tied to cautious decision boundaries—specifically *"Required action not completed"* and *"Reported inability to find or verify information."*
- **Persistent Context-Retrieval Bottlenecks:** The most consistent failure mode across all models was *"Incorrect information or recommendation,"* largely because models struggled to locate and use relevant details buried inside long personal conversation histories:

| Personal Context Source | Average Rubric Win Rate | Key Observation |
| :--- | :--- | :--- |
| **Additional Task Context** | **55.8%** | Drops to **41.5%** when the exact same facts are synthetically inserted into past conversations. |
| **Explicit Memories** | **47.8%** | Moderately accessible compared to raw chat logs. |
| **Past Conversations** | **33.33%** | Inspecting 100%-passing cases showed models often inferred answers from conversation titles or duplicate context elsewhere rather than retrieving facts from the body of past chats. |


- 気づき・疑問：

### LifeVal と現在の評価ワークフローの比較

| 比較軸 | LifeVal（フロンティア・エージェントベンチマーク） | 現在のワークフロー（ドメイン特化型 QA 評価） |
| :--- | :--- | :--- |
| **主な評価対象** | **パーソナライズされたエージェントタスク:** 169のコンシューマー向けシナリオにおいて、個々のユーザー文脈に合わせた複数ステップの行動、ツール利用、推論を評価。 | **根拠に基づく講座・FAQ応答:** 特定の講座シラバス、用語集（`用語集`）、およびフォーマット規則（`第N回`）に対する単発の質疑応答（Q&A）の遵守度を評価。 |
| **規模と参加者の構成** | **複数グループによる人間検証パイプライン:** タスク作成者、ペルソナ提供者、多段階の人間および自動検証者など、異なる役割を持つ複数の参加者グループに依存。 | **単独のアノテーター ＋ LLM 評価器:** 1人のドメイン専門家（あなた）が正解ラベルを作成し、単一の LLM 評価器（`gemini-3.5-flash-lite`）をキャリブレーション（調整）。 |
| **「正解（Ground Truth）」の性質** | **主観的・ペルソナ依存:** タスクが「パーソナライズ」されているため、正しさは個々のユーザーの好みや実際の実行状態に依存し、多段階の人間による検証が必要。 | **ルールベース・決定的:** 正しさは明確な境界線（例：「用語集の範囲を超えて推測・断定しない」「末尾を『第N回』で終える」）によって定義され、ルーブリックや正規表現で明文化が可能。 |
| **主な目的** | **モデル性能の比較・ベンチマーク:** オープンエンドなコンシューマー向けワークフローにおいて、最先端（フロンティア）モデルの絶対的な能力を測定・比較すること。 | **システムとプロンプトの信頼性向上（CI / 評価）:** 自動採点が自身のドメイン判断を高い精度で再現できるよう（一致率70%以上、カバレッジ100%など）、ルーブリックとプロンプトを反復的に改善すること。 |

---

### 重要なポイント

* **LifeVal** は、「単一の普遍的な正解が存在しない状況で、いかにフロンティアモデルの能力を測定するか」という課題に対し、**複数の人間グループに役割を分担させてパーソナライズされた実行結果を検証する**アプローチをとっています。
* 一方、演習のワークフローは **「ルーブリック駆動の評価エンジニアリング（Rubric-Driven Evaluation Engineering）」** です。自身のドメイン知識や直感を明確で決定的なルールへと落とし込み、LLM 評価器にシステムの回帰テスト（リグレッションテスト）を自動実行させるための実践的なアプローチと言えます。
