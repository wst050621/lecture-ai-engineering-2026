import argparse
from google import genai
from google.genai import errors
from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(chat, question: str) -> str:
    # chat オブジェクトが会話履歴を保持するため、過去のやり取りも文脈として送信される
    response = chat.send_message(question)
    # TODO(第1回 演習): response.usage_metadata から
    #   入力トークン数と出力トークン数を表示してみよう（Copilotに頼んでよい）
    if response.usage_metadata:
        print(f"入力トークン数: {response.usage_metadata.prompt_token_count}")
        print(f"出力トークン数: {response.usage_metadata.candidates_token_count}")
        print(f"合計トークン数: {response.usage_metadata.total_token_count}")
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する（会話履歴あり）")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)  # 会話履歴を保持するチャットセッション

    print(f"[model] {MODEL}")
    question = args.question
    print(f"[質問] {question}\n")

    while True:
        try:
            print(ask(chat, question))
        except errors.APIError as e:
            print(api_error_message(e.code, e.message))
            raise SystemExit(1)

        try:
            question = input("\n[次の質問]（空Enter / exit で終了）> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if question.lower() in ("", "exit", "quit"):
            break
        print()


if __name__ == "__main__":
    main()