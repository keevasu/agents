import anyio
from claude_agent_sdk import query, AssistantMessage, TextBlock, ResultMessage

async def main():
    """Simple asynchronous query example with message filtering."""
    print("Asking Claude...")
    
    # The query function is an async generator, allowing for real-time streaming
    async for message in query(prompt="Explain the benefits of asynchronous programming in Python."):
        # Filter for human-readable content from the assistant
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
        
        # Optionally, print the final cost when the task is done
        elif isinstance(message, ResultMessage) and message.total_cost_usd > 0:
            print(f"\nCost: ${message.total_cost_usd:.4f}")

if __name__ == "__main__":
    # anyio.run is used to start the asynchronous event loop
    anyio.run(main)

