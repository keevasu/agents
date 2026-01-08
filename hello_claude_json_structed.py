import anyio
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, TextBlock

async def main():
    # 1. Define the desired JSON structure (schema)
    my_schema = {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
            "tags": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["summary", "sentiment", "tags"]
    }

    # 2. Set output_format in the options
    options = ClaudeAgentOptions(
        output_format={
            "type": "json_schema",
            "json_schema": my_schema
        }
    )

    prompt = "Review this product: 'The camera quality is amazing but the battery dies fast.'"

    # 3. Execute the async query
    async for message in query(prompt=prompt, options=options):
        # Access the validated JSON object directly from the message
        if hasattr(message, "structured_output") and message.structured_output:
            print("Final JSON Response:")
            print(message.structured_output)
        
        elif isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude Reasoning: {block.text}")

if __name__ == "__main__":
    anyio.run(main)

