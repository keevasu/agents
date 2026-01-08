import anyio
import json
import os
from claude_agent_sdk import query, ClaudeAgentOptions, ResultMessage, AssistantMessage, TextBlock

async def main():
    # 1. Create a dummy JSON file in the current directory
    data = {"project": "Agent-SDK", "status": "testing", "version": 2026}
    with open("data.json", "wb") as f:
        f.write(json.dumps(data).encode())

    # 2. Configure the agent to allow reading files
    options = ClaudeAgentOptions(
        allowed_tools=["Read"],  # Give permission to read files
        cwd=os.getcwd()          # Set working directory to current path
    )

    # 3. Instruct the agent to read the specific file
    prompt = "Read the data.json file and summarize its content."

    async for message in query(prompt=prompt, options=options):
        # View Claude's reasoning as it reads the file
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
        
        # Check for the final result
        if isinstance(message, ResultMessage):
            print(f"\nFinal Analysis: {message.result}")

if __name__ == "__main__":
    anyio.run(main)

