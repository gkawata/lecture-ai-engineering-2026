# 第1回 解答

## 演習

- 講座に固有の質問（宿題の3レベル）へのモデルの回答（要約でよい）：AIE2026の宿題における「3レベル」とは、受講生のスキルや目的に応じた3段階の難易度（レベル1：基礎、レベル2：応用、レベル3：発展）の設定を指します


- 用語集の正しい意味と比べて気づいたこと：
      "definition": "AIE2026の宿題の構成。「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階があり、どれか1つに取り組めばその回の宿題は完了。原則として採点はしない。ほぼ正しいと思います。
- 表示できたトークン数（入力 / 出力）：入力トークン数=21 / 出力トークン数=495

## 宿題

- 取り組んだレベル：基礎 / 実装 / 発展 -> 実装に取り組みました。
- やったこと：　app.pyに次のコードを追加
def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
        print(ask(args.question, chat))
        while True:
            question = input("\n[次の質問] (終了するには空行): ")
            if not question:
                break
            print(ask(question, chat))
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


- 結果：1. 共通チャット環境の作成：genai.Client を初期化し、client.chats.create で指定モデル（MODEL）の会話セッション（履歴保持機能）を立ち上げます。

2. 初回質問の実行：設定された質問（引数またはデフォルト値）と作成したチャットセッションを関数に渡し、回答を出力します。

3. 対話型ループの実行：while ループでユーザーからの次の質問を繰り返し待ち受け、空行（Enterのみ）が入力されるまで会話を継続します。


- 気づき・疑問：CodespaceのTerminalはLLMの回答がとても読みずらいです。
