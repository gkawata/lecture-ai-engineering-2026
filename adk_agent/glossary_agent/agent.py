"""ADK version of the AIE2026 learning-support agent.

Usage:
    uv run python -m adk_agent.glossary_agent.agent "What is LoRA?"
    uv run python -m adk_agent.glossary_agent.agent --trace "What is LoRA?"
    uv run python -m adk_agent.glossary_agent.agent --mcp --trace "What is LoRA?"
    uv run python -m adk_agent.glossary_agent.agent --mcp --list-tools
"""

import argparse
import asyncio
import inspect
import json
import os
from pathlib import Path
from typing import get_type_hints

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
    StreamableHTTPConnectionParams,
)
from google.genai import types
from google.genai.errors import APIError
from mcp import StdioServerParameters

from app import tools
from app.config import MODEL, api_error_message, get_api_key

INSTRUCTIONS = """\
あなたはAIエンジニアリング講座（AIE2026）の学習支援エージェントです。
- 用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。
- 回の内容を聞かれたら get_lecture_summary を使う。
- 用語集に見つからないことは、推測で断定せず「用語集にはない」と伝える。
- 回答の最後に、関係する回（第N回）を示す。
- 宿題の答えそのものは書かず、考え方のヒントで導く。
"""

APP_NAME = "glossary_agent"
USER_ID = "cli_user"
MCP_CONFIG = Path(__file__).resolve().parents[2] / "app" / "mcp_servers.json"

root_agent = Agent(
    model=MODEL,
    name="glossary_agent",
    instruction=INSTRUCTIONS,
    tools=[
        tools.search_glossary,
        tools.get_lecture_summary,
        tools.make_quiz,
    ],
)


def load_mcp_servers(config_path: Path = MCP_CONFIG) -> list[McpToolset]:
    """Create ADK MCP toolsets from the shared mcpServers configuration."""
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))["mcpServers"]
    toolsets = []
    for name, spec in config.items():
        if "url" in spec:
            connection_params = StreamableHTTPConnectionParams(url=spec["url"])
        else:
            connection_params = StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=spec["command"],
                    args=spec.get("args", []),
                    env=spec.get("env"),
                )
            )
        toolsets.append(
            McpToolset(
                connection_params=connection_params,
                tool_name_prefix=f"{name}_",
            )
        )
    return toolsets


def build_mcp_agent(toolsets: list[McpToolset]) -> Agent:
    """Use tools published by the configured MCP servers."""
    return Agent(
        model=MODEL,
        name="glossary_agent",
        instruction=INSTRUCTIONS,
        tools=toolsets,
    )


def _python_type_name(annotation: object) -> str:
    return {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
    }.get(annotation, "object")


def _function_parameters(function: object) -> dict:
    hints = get_type_hints(function)
    return {
        "properties": {
            parameter.name: {
                "type": _python_type_name(hints.get(parameter.name, parameter.annotation))
            }
            for parameter in inspect.signature(function).parameters.values()
        }
    }


async def print_tools(toolsets: list[McpToolset]) -> None:
    """Print available tool names, descriptions, and argument schemas."""
    if toolsets:
        tools_seen = []
        for toolset in toolsets:
            tools_seen.extend(await toolset.get_tools())
    else:
        tools_seen = [
            {
                "name": function.__name__,
                "description": inspect.getdoc(function) or "",
                "parameters": _function_parameters(function),
            }
            for function in (
                tools.search_glossary,
                tools.get_lecture_summary,
                tools.make_quiz,
            )
        ]

    print(f"モデルに見えているツール: {len(tools_seen)} 個")
    for tool in tools_seen:
        if isinstance(tool, dict):
            name = tool["name"]
            description = tool["description"]
            schema = tool["parameters"]
        else:
            name = tool.name
            description = tool.description or ""
            schema = getattr(tool, "input_schema", {})
        print(f"\n[{name}]")
        print("  " + inspect.cleandoc(description).replace("\n", "\n  "))
        properties = schema.get("properties", {}) if isinstance(schema, dict) else {}
        print(f"  引数: {json.dumps(properties, ensure_ascii=False)}")


def print_trace(events: list) -> None:
    """Print tool calls, results, and the latest model usage metadata."""
    print("\n--- trace ---")
    usage = None
    for event in events:
        if event.usage_metadata is not None:
            usage = event.usage_metadata
        if event.content is None:
            continue
        for part in event.content.parts or []:
            if part.function_call:
                call = part.function_call
                print(f"[tool call]   {call.name}({json.dumps(call.args, ensure_ascii=False)})")
            elif part.function_response:
                response = part.function_response
                result = str(response.response)
                print(f"[tool return] {response.name} -> {result[:120]}…")
    print(f"[usage] {usage}")


async def run_question(target: Agent, question: str) -> tuple[str, list]:
    session_service = InMemorySessionService()
    runner = Runner(
        agent=target,
        app_name=APP_NAME,
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    events = [
        event
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=session.id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=question)],
            ),
        )
    ]

    final_text = ""
    for event in events:
        if event.is_final_response() and event.content:
            final_text = "".join(
                part.text for part in event.content.parts or [] if part.text
            )
    if not final_text:
        raise RuntimeError("エージェントから最終回答を受け取れませんでした。")
    return final_text, events


async def async_main() -> None:
    parser = argparse.ArgumentParser(description="学習支援エージェントに質問する")
    parser.add_argument("question", nargs="?")
    parser.add_argument("--trace", action="store_true", help="ツール呼び出しを表示する")
    parser.add_argument(
        "--mcp",
        action="store_true",
        help="第5回: ツールを MCP サーバー（app/mcp_servers.json）から受け取る",
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="モデルに見えるツール一覧を表示して終了する（APIキー不要）",
    )
    args = parser.parse_args()

    toolsets = load_mcp_servers() if args.mcp else []
    target = build_mcp_agent(toolsets) if args.mcp else root_agent
    try:
        if args.list_tools:
            await print_tools(toolsets)
            return
        if not args.question:
            parser.error("質問を指定してください")

        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = get_api_key()
        print(f"[model] {MODEL}")
        if args.mcp:
            print("[tools] MCP サーバー（app/mcp_servers.json）")
        try:
            answer, events = await run_question(target, args.question)
        except APIError as error:
            print(api_error_message(error.code, str(error)[:200]))
            raise SystemExit(1) from error
        print(answer)
        if args.trace:
            print_trace(events)
    finally:
        for toolset in toolsets:
            await toolset.close()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
