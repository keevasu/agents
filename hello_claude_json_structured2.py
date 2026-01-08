import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock, ResultMessage

async def main():
    options = ClaudeAgentOptions(
        output_format={
            "type": "json_schema",
            "json_schema": {
                "type": "object",
                "properties": {"answer": {"type": "string"}},
                "required": ["answer"]
            }
        }
    )

    async for message in query(prompt="Say hello in JSON", options=options):
        # 1. Handle text reasoning (The part that caused your error)
        if isinstance(message, AssistantMessage):
            for block in message.content:
                # FIX: Use isinstance() instead of checking a .type attribute
                if isinstance(block, TextBlock):
                    print(f"Claude Reasoning: {block.text}")

        # 2. Handle the final JSON result
        if isinstance(message, ResultMessage):
            print("\n--- FINAL JSON RESULT ---")
            print(message.result)

if __name__ == "__main__":
    anyio.run(main)

